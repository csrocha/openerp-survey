// static/src/js/widgets.js
function openerp_zondaggio_widgets(instance, module){
    var QWeb = instance.web.qweb,
	_t = instance.web._t;

    module.questionnaire_ui = instance.web.Widget.extend({
        events: {
            'change input': 'on_change',
            'click button.do_save': 'do_save',
        },
        template: 'StyledView',
        init:function(parent,options){
                this._super(parent);
                options = options || { context: {} };
                this.session.questionnaire_context = options.context;
                this.session.questionnaire_params = options.params;
                this.is_fullscreen = options.params && options.params.fullscreen || false;
                this.questionnaire = new module.Questionnaire(this.session);
                this.questionnaire_widget = this;
            },
        start:function() {
            var self=this;
            return self.questionnaire.ready.done(function(){
                self.renderElement();
                // TODO: Load values
            });
        },
        get_name:function() {
            if (this.questionnaire.get('survey') == null) {
                return 'No defined'
            } else {
                return this.questionnaire.get('survey').name;
            }
        },
        get_description:function() {
            if (this.questionnaire.get('survey') == null) {
                return 'No defined'
            } else {
                return this.questionnaire.get('survey').description;
            }
        },
        get_nodes:function() {
            if (this.questionnaire.get('nodes') == null) {
                return []
            } else {
                return this.questionnaire.get('nodes');
            }
        },
        get_pages:function() {
            if (this.questionnaire.get('pages') == null) {
                return []
            } else {
                return this.questionnaire.get('pages');
            }
        },
        get_complete_places:function(node_id) {
            return this.questionnaire.get('node_complete_places')[node_id];
        },
        do_save:function(e) {
            var button = e.currentTarget;
            var data = {};
            var items = $('textarea, input');
            for (item in items) {
                var widget = items[item];
                if (widget.classList && widget.classList.length > 0) {
                   data[widget.classList[0]] = widget.value;
                };
            };
            this.questionnaire.save_server_data(data);
            this.go_next(button.parentNode);
        },
        go_prev:function(actual) {
            var next = actual.previousElementSibling;
            if (next) {
                next.scrollIntoView();
            }
        },
        go_next:function(actual) {
            var next = actual.nextElementSibling;
            if (next) {
                next.scrollIntoView();
            }
        },
        on_change:function(e) {
            var input_id = e.currentTarget.classList[0];
            // check if input enable of disable something.
            this.evaluate_conditions();
            e.stopPropagation();
        },
        evaluate_conditions:function() {
            var node_conditions = this.questionnaire.get('node_conditions');

            for (var key in node_conditions) {
                var condition = node_conditions[key];
                var control = $(_.str.sprintf(".inp_%s", this.get_complete_places(key)))[0];
                var input = $(_.str.sprintf(".inp_%s", this.get_complete_places(condition.node_id)))[0];
                var value = input.value;
                if (input.type == "checkbox") {
                    value = input.checked;
                };
                var statement = _.str.sprintf("%s %s %s", value, condition.operator, condition.value);
                control.disabled = !eval(statement);
            };
        },
    })

};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
