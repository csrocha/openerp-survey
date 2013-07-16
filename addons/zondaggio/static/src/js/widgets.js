// static/src/js/widgets.js
function openerp_zondaggio_widgets(instance, module){
    var QWeb = instance.web.qweb,
	_t = instance.web._t;

    module.questionnaire_ui = instance.web.Widget.extend({
        events: {
            'change input': 'on_change',
            'click button.do_save': 'do_save',
            'click button.do_print': 'do_print',
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
                self.load_data();
                self.evaluate_conditions();
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
        get_complete_places:function() {
            return this.questionnaire.get('node_complete_places');
        },
        load_data:function() {
            var answers = this.questionnaire.get('answers');
            var complete_place_nodes = this.questionnaire.get('complete_place_nodes');
            // Input text type and text area.
            var items = $("input[type='text'][class^='inp_'],input[type='hidden'][class^='inp_'],textarea[class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                var id = widget.classList[0].replace(/^inp_/,'');
                var question_id = complete_place_nodes[id];
                widget.value = answers[question_id].input || '';
                widget.disabled = answers[question_id].state != 'enabled';
            });
            // Booleans or checkbox.
            var items = $("input[type='checkbox'][class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                var id = widget.classList[0].replace(/^inp_/,'');
                var question_id = complete_place_nodes[id];
                widget.checked = answers[question_id].input;
                widget.disabled = answers[question_id].state != 'enabled';
            });
            // Update on selects.
            var items = $("input[type='hidden'][class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                if (widget.value != "false") {
                    var radios = $(_.str.sprintf('input[type="radio"][name="%s"][alt="%s"]', widget.classList[0],widget.value))
                    radios.each(function(item) { radios[item].checked = true; });
                }
            });
        },
        save_data:function() {
            var data = {};
            // Input text type and text area.
            var items = $("input[type='text'][class^='inp_'],input[type='hidden'][class^='inp_'],textarea[class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                data[widget.classList[0]] = widget.value;
            });
            // Booleans or checkbox.
            var items = $("input[type='checkbox'][class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                data[widget.classList[0]] = widget.checked;
            });
            this.questionnaire.save_server_data(data);
        },
        do_save:function(e) {
            var button = e.currentTarget;
            this.save_data();
            this.go_next(button.parentNode);
        },
        do_print:function(e) {
            window.print();
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
            this.on_change_select_one(e.currentTarget);
            this.evaluate_conditions();
            e.stopPropagation();
        },
        on_change_select_one:function(widget){
            if (widget.type=='radio') {
                var widget_parent = $(_.str.sprintf("input[type='hidden'][class='%s']", widget.name))[0];
                widget_parent.value = widget.alt;
            }
        },
        evaluate_conditions:function() {
            var node_conditions = this.questionnaire.get('node_conditions');
            var complete_places = this.questionnaire.get('node_complete_places');
            var solved_nodes = {};

            // Solve boolean statements
            for (var key in node_conditions) {
                for (var i in node_conditions[key]) {
                    var condition = node_conditions[key][i];
                    var input = $(_.str.sprintf(".inp_%s", complete_places[condition.node_id]))[0];

                    if (input == null) continue;

                    var value = input.value;
                    if (input.type == "checkbox") {
                        value = input.checked;
                    };
                    var not = (condition.operator.indexOf('not') >= 0) && '!' || '';
                    var oper = condition.operator.replace(/not /,'');
                    var statement = _.str.sprintf("%s('%s' %s %s)", not, value, oper, condition.value);
                    var complete_place = complete_places[key];
                    if (!(complete_place in solved_nodes)) {
                        solved_nodes[complete_place] = !eval(statement);
                    } else {
                        solved_nodes[complete_place] = solved_nodes[complete_place] || !eval(statement);
                    };
                };
            };
            // Asign state
            for (complete_place in solved_nodes) {
                var control = $(_.str.sprintf(".inp_%s", complete_place))[0];
                var childs = $(_.str.sprintf("input[name='inp_%s']", complete_place));
                control.disabled = solved_nodes[complete_place];
                childs.each(function(node){ childs[node].disabled = control.disabled; });
            };
        },
    })

};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
