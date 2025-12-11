odoo.define('pest_control.custom_buttons', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');

    var _t = core._t;

    FormController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            if (this.modelName === 'pest.control.site.visit') {
                var self = this;

                // Add Send Email Button
                var $sendEmailButton = $('<button>')
                    .text(_t('Send Email'))
                    .addClass('btn btn-primary o_pest_control_send_email')
                    .on('click', function () {
                        self._rpc({
                            model: 'pest.control.site.visit',
                            method: 'action_send_site_visit_email',
                            args: [[self.handle.getActiveId()]],
                            context: self.initialState.context,
                        }).then(function () {
                            self.displayNotification({
                                title: _t('Success'),
                                message: _t('Email sent successfully.'),
                                type: 'success',
                            });
                        }).catch(function (error) {
                            self.displayNotification({
                                title: _t('Error'),
                                message: error.data.message || _t('Failed to send email.'),
                                type: 'danger',
                            });
                        });
                    });

                // Add Add to Calendar Button
                var $addToCalendarButton = $('<button>')
                    .text(_t('Add to Calendar'))
                    .addClass('btn btn-primary o_pest_control_add_to_calendar')
                    .on('click', function () {
                        self._rpc({
                            model: 'pest.control.site.visit',
                            method: 'action_create_calendar_event',
                            args: [[self.handle.getActiveId()]],
                            context: self.initialState.context,
                        }).then(function () {
                            self.displayNotification({
                                title: _t('Success'),
                                message: _t('Event added to calendar successfully.'),
                                type: 'success',
                            });
                        }).catch(function (error) {
                            self.displayNotification({
                                title: _t('Error'),
                                message: error.data.message || _t('Failed to add event to calendar.'),
                                type: 'danger',
                            });
                        });
                    });

                // Append buttons to the control panel
                this.$buttons.append($sendEmailButton).append($addToCalendarButton);
            }
        },
    });
});
