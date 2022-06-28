odoo.define("pos_credit_limit.credit", function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');

    models.load_fields('res.partner',['blocking_stage','credit','warning_stage','active_limit', 'parent_id']);
    models.load_fields('pos.payment.method',['is_cash_count','journal_id']);
    models.load_models({
        model:  'account.journal',
        fields: ['pos_credit'],
        domain: [['pos_credit','=',true]],
        loaded: function(self, credit_journals){
            self.credit_journals = credit_journals;
        },
    });

    const CreditDetails = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
            }
            addNewPaymentLine({ detail: paymentMethod }) {
                var self = this;
                var current_order = this.currentOrder;
                var credit_journal = false;
                if (paymentMethod.journal_id) {
                    for(var i=0;i < this.env.pos.credit_journals.length;i++){
                        if (this.env.pos.credit_journals[i].id == paymentMethod.journal_id[0]) {
                            credit_journal = true;
                        }
                    }
                    if (credit_journal) {
                        if (!current_order.attributes.client){
                            self.select_customer(self);
                            return false;
                        } else {
                            if (current_order.attributes.client.active_limit){
                                if (current_order.attributes.client.blocking_stage < current_order.attributes.client.credit){
                                    self.showPopup('ErrorPopup',{
                                        title: self.env._t("Exceeded Credit Limit"),
                                        body: self.env._t("Sorry you have exceeded your Credit Limit , Please use another Payment Method or Contact Manager "),
                                    });
                                    return false;
                                }
                                else{
                                    self.changePaymentLine(self, paymentMethod);
                                }
                            }
                             else {
                                self.showPopup('ErrorPopup',{
                                    title: self.env._t("Customer not eligible for Credit Payment"),
                                    body: self.env._t("Please contact manager if this is an error"),
                                });
                                return false;
                            }
                        }
                    } else {
                        self.changePaymentLine(self, paymentMethod);
                    }
                } else {
                    self.changePaymentLine(self, paymentMethod);
                }
            }
            async changePaymentLine (self, paymentMethod) {
                if (self.currentOrder.electronic_payment_in_progress()) {
                    self.showPopup('ErrorPopup', {
                        title: self.env._t('Error'),
                        body: self.env._t('There is already an electronic payment in progress.'),
                    });
                    return false;
                } else {
                    self.currentOrder.add_paymentline(paymentMethod);
                    NumberBuffer.reset();
                    self.payment_interface = paymentMethod.payment_terminal;
                    if (self.payment_interface) {
                        self.currentOrder.selected_paymentline.set_payment_status('pending');
                    }
                    console.log("payment method ", self.currentOrder.selected_paymentline);
                    return true;
                }
            }
            async select_customer (self) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Please select the Customer'),
                    body: this.env._t('You need to select a customer for using this Payment Method.'),
                });
                if (confirmed) {
                    this.selectClient();
                }
            }
            async _isOrderValid(isForceValidate) {
                var self = this;
                var order = this.env.pos.get_order();
                if (this.currentOrder.get_orderlines().length === 0 && this.currentOrder.is_to_invoice()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Empty Order'),
                        body: this.env._t(
                            'There must be at least one product in your order before it can be validated and invoiced.'
                        ),
                    });
                    return false;
                }

                const splitPayments = this.paymentLines.filter(payment => payment.payment_method.split_transactions)
                if (splitPayments.length && !this.currentOrder.get_client()) {
                    const paymentMethod = splitPayments[0].payment_method
                    const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Customer Required'),
                        body: _.str.sprintf(this.env._t('Customer is required for %s payment method.'), paymentMethod.name),
                    });
                    if (confirmed) {
                        this.selectClient();
                    }
                    return false;
                }

                if ((this.currentOrder.is_to_invoice() || this.currentOrder.is_to_ship()) && !this.currentOrder.get_client()) {
                    const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Please select the Customer'),
                        body: this.env._t(
                            'You need to select the customer before you can invoice or ship an order.'
                        ),
                    });
                    if (confirmed) {
                        this.selectClient();
                    }
                    return false;
                }
                for(var i=0;i < order.paymentlines.length;i++){
                    var credit_journal = false;
                    if (order.paymentlines.models[i].payment_method.journal_id) {
                        for(var j=0;j < this.env.pos.credit_journals.length;j++){
                            if (this.env.pos.credit_journals[j].id == order.paymentlines.models[i].payment_method.journal_id[0]) {
                                credit_journal = true;
                            }
                        }
                        if (credit_journal) {
                            if (order.attributes.client.active_limit){
                                var temp_credit = order.attributes.client.credit;
                                temp_credit += order.paymentlines.models[i].amount;
                                if(order.attributes.client.blocking_stage >= temp_credit){
                                    if(order.attributes.client.warning_stage<= temp_credit){
                                        alert("Credit is exceeding the warning limit.\n\n Current Credit is : "+order.attributes.client.credit+".\n\n Credit Limit : "+order.attributes.client.blocking_stage+"")
                                    }
                                    order.attributes.client.credit = temp_credit;
                                    self.toggleIsToInvoice();
                                }
                                else{
                                    this.showPopup('ErrorPopup',{
                                        title: this.env._t("Exceeding Credit Limit"),
                                        body: this.env._t(['Sorry the credit allowed will reach its limit(Credit Limit :' +order.attributes.client.blocking_stage+').',
                                                            '\nYour current credit is('+order.attributes.client.credit+').',
                                                            'Please pay using a different Payment Method or Contact manager'].join(' ')),
                                        });
                                        return false;
                                }
                            }
                            else {
                                self.showPopup('ErrorPopup',{
                                    title: self.env._t("Customer not eligible for Credit Payment"),
                                    body: self.env._t("Please contact manager if this is an error"),
                                });
                                return false;
                            }
                        }
                    }
                }

                var customer = this.currentOrder.get_client()
                if (this.currentOrder.is_to_ship() && !(customer.name && customer.street && customer.city && customer.country_id)) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Incorrect address for shipping'),
                        body: this.env._t('The selected customer needs an address.'),
                    });
                    return false;
                }

                if (!this.currentOrder.is_paid() || this.invoicing) {
                    return false;
                }

                if (this.currentOrder.has_not_valid_rounding()) {
                    var line = this.currentOrder.has_not_valid_rounding();
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Incorrect rounding'),
                        body: this.env._t(
                            'You have to round your payments lines.' + line.amount + ' is not rounded.'
                        ),
                    });
                    return false;
                }

                // The exact amount must be paid if there is no cash payment method defined.
                if (
                    Math.abs(
                        this.currentOrder.get_total_with_tax() - this.currentOrder.get_total_paid()  + this.currentOrder.get_rounding_applied()
                    ) > 0.00001
                ) {
                    var cash = false;
                    for (var i = 0; i < this.env.pos.payment_methods.length; i++) {
                        cash = cash || this.env.pos.payment_methods[i].is_cash_count;
                    }
                    if (!cash) {
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Cannot return change without a cash payment method'),
                            body: this.env._t(
                                'There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'
                            ),
                        });
                        return false;
                    }
                }

                // if the change is too large, it's probably an input error, make the user confirm.
                if (
                    !isForceValidate &&
                    this.currentOrder.get_total_with_tax() > 0 &&
                    this.currentOrder.get_total_with_tax() * 1000 < this.currentOrder.get_total_paid()
                ) {
                    this.showPopup('ConfirmPopup', {
                        title: this.env._t('Please Confirm Large Amount'),
                        body:
                            this.env._t('Are you sure that the customer wants to  pay') +
                            ' ' +
                            this.env.pos.format_currency(this.currentOrder.get_total_paid()) +
                            ' ' +
                            this.env._t('for an order of') +
                            ' ' +
                            this.env.pos.format_currency(this.currentOrder.get_total_with_tax()) +
                            ' ' +
                            this.env._t('? Clicking "Confirm" will validate the payment.'),
                    }).then(({ confirmed }) => {
                        if (confirmed) this.validateOrder(true);
                    });
                    return false;
                }

                if (!this._isValidEmptyOrder()) return false;

                return true;
            }

//            payDebt(){
//                console.log('payDebt');
//                this.currentOrder.add_product(this.env.pos.db.get_product_by_barcode('DP001'), {
//                    quantity: 1,
//                    price: 0,
//                });
//                for (var i = 0; i < this.currentOrder.get_paymentlines().length; i++) {
//                    if (this.currentOrder.get_paymentlines()[i].payment_method.journal.debt) {
//                        this.currentOrder.get_paymentlines()[i].destroy();
//                    }
//                }
//                console.log("client ", this.env.pos.payment_methods);
//                for (var i = 0; i < this.env.pos.payment_methods.length; i++) {
//                    if (this.env.pos.payment_methods[i].name == 'Credit') {
//                        var payment_method = this.env.pos.payment_methods[i];
//                    }
//                }
//                if (this.currentOrder.get_client()) {
//                    var credit = this.currentOrder.get_client().credit;
//                    var paydebtline = new models.Paymentline({}, {
//                        pos: this.env.pos,
//                        order: this.currentOrder,
//                        payment_method: payment_method
//                    });
//                    paydebtline.set_amount(credit);
//                    this.currentOrder.add_paymentline(paydebtline);
//                }
//
////                this.render();
//            }
        };

    Registries.Component.extend(PaymentScreen, CreditDetails);

    return CreditDetails;

});