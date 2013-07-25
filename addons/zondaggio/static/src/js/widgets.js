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
        template: 'QuestionnaireView',
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
                self.dynamicCss();
                self.load_data();
                self.evaluate_conditions();
            });
        },
        dynamicCss:function() {
            /* Remove inner labels for tables */
            // var divs = $('div.group .zoe_selectone:not(:first-child) .zoe_col_label');
            var divs = $('div.group .zoe_selectone+.zoe_selectone:not(.zoe_section_description) .zoe_col_label');
            divs.remove();
            /* Put especificar in otros */
            var esp = $('div.zoe_especificar');
            $('div.zoe_otros div.zoe_row_label').append(function(index, item) {
                return esp[index];
            });
            /* */
            $('.zoe_section_description.zoe_selectone:not(.zoe_transpose)').prepend(function(index, item){
                return jQuery(item).find('.zoe_row_label');
            })
            $('.zoe_section_description.zoe_selectone:not(.zoe_transpose) .zoe_question .zoe_row_label').remove()
            $('.zoe_selectone.zoe_section_description:not(.zoe_transpose)>.zoe_col_label>.label').remove()
            /* Remove labels transpose */
            $('.zoe_selectone.zoe_transpose+.zoe_selectone.zoe_transpose>.zoe_question>.option>.zoe_label').remove()
            $('.zoe_selectone.zoe_transpose+.zoe_selectone.zoe_transpose>.zoe_label>.option>.zoe_label').remove()
            /* Same height for every-one*/
            //var _h = 0; $('.zoe_selectone.zoe_transpose .zoe_option').height(function(idx, h){ if(_h < h) _h = h; }).height(_h);
            $('.group .zoe_selectone.zoe_transpose:first-child').each(function(idx, item){
                _h = 0;
                jQuery(item).find('.option');
            })

        },
        push_parent:function(node) {
            this.actual_parent.push(node.parent_id);
        },
        get_name:function() {
            if (this.questionnaire.get('survey') == null) {
                return 'Encuesta Nacional Sobre Valoración de la Innovación y Conocimiento de Fondos de Financiamiento'
            } else {
                return this.questionnaire.get('survey').name;
            }
        },
        get_description:function() {
            if (this.questionnaire.get('survey') == null) {
                return '<p>Las respuestas que Ud. nos provea serán estrictamente secretas y sólo se utilizarán con fines estadísticos (Ley 17.622 Art. 10° de secreto estadístico). Los datos serán publicados exclusivamente en compilaciones de conjunto, de modo que no pueda ser violado el secreto comercial o patrimonial, ni individualizarse las personas o entidades a quienes se refieran.</p><p>Una vez finalizado el relevamiento, le remitiremos de forma personal los resultados e informes de prensa elaborados a partir de la información recogida.</p><p>Le agradecemos su valiosa colaboración brindándonos su tiempo y sus respuestas.</p><h2>En este momento se está cargando el cuestionario.</h2>'
            } else {
                return this.questionnaire.get('survey').description;
            }
        },
        get_widgets:function() {
            return this.questionnaire.get('widgets');
        },
        get_root:function() {
            return this.questionnaire.get('root');
        },
        get_childs:function(node) {
            if (node in this.questionnaire.get('tree')) {
                return this.questionnaire.get('tree')[node];
            } else {
                return [];
            }
        },
        filter_nodes_by_type:function(items, eq_type, neq_type) {
            var r = [];
            var nodes=this.questionnaire.get('node_dict');
            for (item in items) {
                var node = nodes[items[item]];
                if ((eq_type.indexOf(node.type) >= 0) || !(neq_type.indexOf(node.type) >= 0 )) {
                    r.push(items[item]);
                }
            };
            return r;
        },
        get_node_dict:function() {
            if (this.questionnaire.get('node_dict') == null) {
                return {}
            } else {
                return this.questionnaire.get('node_dict');
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
                if (control) {
                    control.disabled = solved_nodes[complete_place];
                    childs.each(function(node){ childs[node].disabled = control.disabled; });
                } else {
                    console.log("Cant found:",_.str.sprintf(".inp_%s", complete_place));
                    debugger;
                }
            };
        },
        get_table:function(root) {
            var nodes = this.questionnaire.get('nodes');
            var node_dict = this.questionnaire.get('node_dict');
            var tree = this.questionnaire.get('tree');

            get_dim = function(root) {
                var dim = [];
                root.child_ids.forEach(function(item){
                        dim.push(item);
                });
                return dim;
            };

            var dim = [];
            var node = root;
            while(node.child_ids.length > 0) {
                dim.push(get_dim(node));
                node = node_dict[node.child_ids[0]];
            };

            build_table = function(root) {
                var table = { };
                root.child_ids.forEach(function(item){
                    table[node_dict[item].name] = build_table(node_dict[item]);
                });
                if (jQuery.isEmptyObject(table)) {
                    return root;
                } else {
                    return table;
                }
            };

            var table=build_table(root);

            return {
                nodes: node_dict,
                table: table,
                dim: dim,
                get: function(keys) {
                    var self=this;
                    var node=null;
                    keys.forEach(function(item){
                         name = self.nodes[item].name;
                         if (node == null) {
                             node = table[name];
                         } else {
                             node = node[name];
                         }
                    });
                    return node;
                },
            };
        }, 
    })

};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
