// static/src/js/widgets.js
function openerp_zondaggio_widgets(instance, module){
    var QWeb = instance.web.qweb,
	_t = instance.web._t;

    module.questionnaire_ui = instance.web.Widget.extend({
        events: {
            'change input': 'on_change',
            'click input': 'on_change', /* Fucking IE */
            'change textarea': 'on_change',
            'click textarea': 'on_change', /* Fucking IE */
            'click button.do_start': 'do_save',
            'click button.do_save': 'do_save',
            'click button.do_cont': 'do_save',
            'click button.do_prev': 'go_prev',
            'click button.do_print': 'do_print',
            'click button.do_done': 'do_done',
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
                self.calc_globals();
                self.update_workflow('start');
            });
        },
	update_workflow:function(moment) {
            var self = this;
	    var state=self.questionnaire.get('questionnaire').state;
	    switch (moment + '|' + state) {
            case 'start|draft':
                self.questionnaire.send_signal('sgn_begin').then(function(){
			    return self.questionnaire.send_signal('sgn_wait');
		});
		break;
            case 'start|complete':
                $('.zoe_active').removeClass('zoe_active').addClass('zoe_inactive');
		$('.zoe_closed').removeClass('zoe_inactive').addClass('zoe_active')
		$('div.zoe_title>div>*').remove();
		$('button').addClass('zoe_hidden');
		break;
	    case 'on_change|waiting':
		self.has_change = true;
		break;
	    case 'save|waiting':
		if (self.has_change) self.questionnaire.send_signal('sgn_continue');
		break;
	    case 'on_close|in_progress':
		self.questionnaire.send_signal('sgn_end');
		break;
	    }
	},
        dynamicCss:function() {
            /* Acomodar tabla P2 */
            $('table.zoe:first').prepend('<tr><td rowspan="2"><p style="text-align:center">Problemas</p></td><td colspan="10" class="zoe_arrow"><div class="zoe_left_arrow"><p style="display:inline">Nada relevante</p></div><div class="zoe_right_arrow"><p style="display:inline">Muy relevante</p></div></td></tr>');
            $('.zoe_vicff_a_2 table>tbody>tr>th:first').remove();
	    $('.zoe_vicff_a_2 table>tbody>tr>th.zoe_row_continue>p').css('textAlign','left');
            /* Acomodar P3 */
	    $('.zoe_vicff_b_3 table tr:first').css('display','none');
	    /* Acomodar P8 */
	    $('.zoe_vicff_b_8 table th:first').html('<p>Forma jurídica</p>');
	    /* Acomodar P9 */
	    $('.zoe_vicff_b_9 table th:first').html('<p>Fase</p>');
	    /* Acomodar P12 */
	    $('.zoe_vicff_b_12 table th:first').html('<p>Normas de calidad</p>');
	    /* Acomodar P14 */
	    $('.zoe_vicff_b_14 table th:first').html('<p>Máximo nivel de formación alcanzado</p>');
	    /* Acomodar P17 */
	    $('.zoe_vicff_c_17 table th:first').html('<p>Motivaciones</p>');
	    /* Acomodar P18 */
	    $('.zoe_vicff_c_18 table th:first').html('<p>Tipo de innovación</p>');
	    /* Acomodar P19 */
	    $('.zoe_vicff_d_19 table th:first').html('<p>Líder/ejecutor de las actividades de innovación</p>');
	    /* Acomodar P25 */
	    $('.zoe_vicff_f_25 table th:first').html('<p>Conductas</p>');
	    /* Acomodar P27 */
	    $('.zoe_vicff_f_27 table th:first').html('<p>Afirmaciones</p>');
	    /* Acomodar P28 */
	    $('.zoe_vicff_f_28 table th:first').html('<p>Actividades</p>');
	    /* Set limits to variables */
            $('input.type_year').numeric({ decimal : false, negative : false }, function() { alert("Solo años"); this.value = "2013"; this.focus(); });
            $('input.type_integer').numeric({ decimal : false, negative : false }, function() { alert("Solo números enteros"); this.value = "0"; this.focus(); });
            $('input.type_porcentual').numeric({ decimal : ',', negative : false }, function() { alert("Solo números reales"); this.value = "0"; this.focus(); });
	    
            /* Remove inner labels for tables */
            // var divs = $('div.group .zoe_selectone:not(:first-child) .zoe_col_label');
            var divs = $('div.group .zoe_selectone+.zoe_selectone:not(.zoe_section_description) .zoe_col_label');
            divs.remove();
            /* Put especificar in otros */
            var esp = $('div.zoe_especificar input');
	    var otr = $('.zoe_otros').find('p:first');
	    otr.parent().prepend(function(index,item) { return esp[index]; });
            otr.hide();
	    esp.attr('placeholder', 'Otro/a (especificar)');
            $('.zoe_especificar').hide();
	    $('.zoe_otros').find('input[type="text"]').css('width','95%');
	    /****
            $('th.zoe_otros,div.zoe_otros>div.zoe_label').prepend(function(index, item) {
                return esp[index];
            });
            $('th.zoe_otros p,div.zoe_otros>p,div.zoe_otros>div>p').hide();
            $('div.zoe_especificar>div>p').hide();
            $('th.zoe_otros input, div.zoe_otros input[type="text"]').attr('placeholder',
			    'Otro/a (especificar)');
            $('th.zoe_otros input').css('width','95%');
	    *****/
            /* Assign parameters to values by default */
            var parameters = this.questionnaire.get('parameters');
            $.each(parameters, function(key, value){
                $(_.str.sprintf("input.var_%s",key)).attr('placeholder',value);
            });
            /* Page setup */
            var page_numbers = $(".zoe_page").length-2;
            var page_active = 0;
            this.active_page(page_active);
            var self=this;
            $(".zoe_progressbar").slider({
                value: page_active,
                min: 1,
                max: page_numbers,
                change: function() {
                    self.active_page($(this).slider("value"));
                }
            });
        },
        active_page:function(page_idx) {
            $('.zoe_active').removeClass('zoe_active').addClass('zoe_inactive');
            var page = $(_.str.sprintf('.zoe_page:eq(%s)', page_idx));
            page.removeClass('zoe_inactive').addClass('zoe_active');
            page.parents('.zoe_title').removeClass('zoe_inactive').addClass('zoe_active');
            this.actual_page=page_idx;
	    /*
	     * If the first page, remove Back button
	     * */
	    var page = $(_.str.sprintf('.zoe_page:eq(%s)', this.actual_page));
            var actual_page = page.index('.zoe_page');
            var search_prefix = _.str.sprintf('.zoe_page:lt(%s)', actual_page)
            var select_page=[];
            /* Search for input */
            var next_page = $('.zoe_page').index($(search_prefix + ' input:enabled:last').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* Search for textarea */
            var next_page = $('.zoe_page').index($(search_prefix + ' textarea:enabled:last').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* keep button */
            if (select_page.length > 0) {
            	$('.do_prev').removeClass('zoe_hidden');
	    } else {
            	$('.do_prev').addClass('zoe_hidden');
	    }
	    /*
	     * If the last page, remove next button, shot done button.
	     * */
            var page = $(_.str.sprintf('.zoe_page:eq(%s)', this.actual_page));
            var actual_page = page.index('.zoe_page');
            var search_prefix = _.str.sprintf('.zoe_page:gt(%s)', actual_page)
            var select_page=[];
            /* Search for input */
            var next_page = $('.zoe_page').index($(search_prefix + ' input:enabled:first').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* Search for textarea */
            var next_page = $('.zoe_page').index($(search_prefix + ' textarea:enabled:first').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* show next or done buttons */
            if (select_page.length > 0) {
            	$('.do_save').removeClass('zoe_hidden');
            	$('.do_done').addClass('zoe_hidden');
	    } else {
            	$('.do_save').addClass('zoe_hidden');
            	$('.do_done').removeClass('zoe_hidden');
	    }
            /*
             * If first page, hide .do_save and show .do_cont
             * */
            if (actual_page == 0) {
            	$('.do_save').addClass('zoe_hidden');
            	$('.do_cont').removeClass('zoe_hidden');
            } else {
            	$('.do_cont').addClass('zoe_hidden');
            }
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
        get_header:function() {
            if (this.questionnaire.get('survey') == null)
                return "<div></div>";
            else
                return this.questionnaire.get('survey').header;
        },
        get_footer:function() {
            if (this.questionnaire.get('survey') == null)
                return "<div></div>";
            else
                return this.questionnaire.get('survey').footer;
        },
	get_closed:function() {
            if (this.questionnaire.get('survey') == null)
                return "<div></div>";
            else {
                return this.questionnaire.get('survey').closed_message;
	    }
        },
	get_goodbye:function() {
            if (this.questionnaire.get('survey') == null)
                return "<div></div>";
	    else 
		return this.questionnaire.get('survey').last_message;
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
                if (node && ((eq_type.indexOf(node.type) >= 0) || !(neq_type.indexOf(node.type) >= 0 ))) {
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
            var variable_nodes = this.questionnaire.get('variable_nodes');
            // Input text type and text area.
            var items = $("input[type='number'][class^='inp_'],input[type='text'][class^='inp_'],input[type='hidden'][class^='inp_'],textarea[class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                var id = widget.classList[0].replace(/^inp_/,'');
                var question_id = variable_nodes[id];
                if (question_id in answers) {
		    var default_value = '';
                    widget.value = answers[question_id].input || default_value;
                    widget.disabled = answers[question_id].state != 'enabled';
                } else {
                    $(widget).css('background-color', 'red');
                    widget.disabled = true;
                }
            });
            // Booleans or checkbox.
            var items = $("input[type='checkbox'][class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                var id = widget.classList[0].replace(/^inp_/,'');
                var question_id = variable_nodes[id];
                if (question_id in answers) {
                    widget.checked = answers[question_id].input;
                    widget.disabled = answers[question_id].state != 'enabled';
                } else {
                    $(widget).css('background-color', 'red');
                    widget.disabled = true;
                }
            });
            // Update on selects.
            var items = $("input[type='hidden'][class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                if (widget.value != "false") {
                    var radios = $(_.str.sprintf('input[type="radio"][name="%s"][alt="%s"]', widget.classList[0],widget.value))
                    radios.each(function(item) { radios[item].checked = true; });
                }
                // Enable or Disable checkbox
                var radios = $(_.str.sprintf('input[type="radio"][name="%s"]', widget.classList[0],widget.value))
                radios.each(function(item) { radios[item].disabled = widget.disabled; });
            });
        },
        save_data:function() {
            var data = {};
            // Input text type and text area.
            var items = $("input[type='number'][class^='inp_'],input[type='text'][class^='inp_'],input[type='hidden'][class^='inp_'],textarea[class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                data[widget.classList[0]] = widget.value;
                data[widget.classList[0].replace(/^inp_/,'sta_')] = (widget.disabled && 'disabled') || 'enabled';
            });
            // Booleans or checkbox.
            var items = $("input[type='checkbox'][class^='inp_']");
            items.each(function(item){
                var widget = items[item];
                data[widget.classList[0]] = widget.checked;
                data[widget.classList[0].replace(/^inp_/,'sta_')] = (widget.disabled && 'disabled') || 'enabled';
            });
            this.questionnaire.save_server_data(data);
            this.update_workflow('save');
        },
        do_save:function(e) {
            var button = e.currentTarget;
            this.save_data();
            this.go_next(button);
        },
        do_print:function(e) {
            window.print();
        },
	do_done:function(e) {
            this.save_data();
            var r=confirm("ATENCIÓN:\nSi 'Acepta' guardar y finalizar la encuesta no podrá volver a ingresar a este cuestionario.\n");
	    if (r==true) {
		    this.questionnaire.send_signal('sgn_end');
                    $('.zoe_active').removeClass('zoe_active').addClass('zoe_inactive');
		    $('.zoe_goodbye').removeClass('zoe_inactive').addClass('zoe_active')
		    $('div.zoe_title>div>*').remove();
		    $('button').addClass('zoe_hidden');
		    $('div.zoe_title>div:first').html('<div class="zoe_page">'+this.get_goodbye()+'</div>');
	    }
	},
        go_prev:function(actual) {
            var page = $(_.str.sprintf('.zoe_page:eq(%s)', this.actual_page));
            var actual_page = page.index('.zoe_page');
            var search_prefix = _.str.sprintf('.zoe_page:lt(%s)', actual_page)
            var select_page=[];
            /* Search for input */
            var next_page = $('.zoe_page').index($(search_prefix + ' input:enabled:last').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* Search for textarea */
            var next_page = $('.zoe_page').index($(search_prefix + ' textarea:enabled:last').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* If I can jump, then jump */
            if (select_page.length > 0) {
                actual_page = Math.max.apply(Math, select_page);
            }
            this.active_page(actual_page);
            $(".zoe_progressbar").slider({value: actual_page});
        },
        go_next:function(actual) {
	    not_missings=$('.zoe_page.zoe_active input:enabled[value!=""],.zoe_page.zoe_active textarea:enabled[value!=""]')
            if (!(not_missing)) {
               self.do_warn('Quedan preguntas sin responder', 'Por favor, completelas antes de continuar.');
               return;
	    }
            var page = $(_.str.sprintf('.zoe_page:eq(%s)', this.actual_page));
            var actual_page = page.index('.zoe_page');
            var search_prefix = _.str.sprintf('.zoe_page:gt(%s)', actual_page)
            var select_page=[];
            /* Search for input */
            var next_page = $('.zoe_page').index($(search_prefix + ' input:enabled:first').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* Search for textarea */
            var next_page = $('.zoe_page').index($(search_prefix + ' textarea:enabled:first').parents('.zoe_page'));
            if (next_page >= 0) { select_page.push(next_page); };
            /* If I can jump, then jump */
            if (select_page.length > 0) {
                actual_page = Math.min.apply(Math, select_page);
	    };
            this.active_page(actual_page);
            $(".zoe_progressbar").slider({value: actual_page});
        },
        on_change:function(e) {
            var input_id = e.currentTarget.classList[0];
            // check if input enable of disable something.
            this.on_change_select_one(e.currentTarget);
            this.evaluate_conditions();
            this.calc_globals();
            e.stopPropagation();
	    this.update_workflow('on_change');
        },
        on_change_select_one:function(widget){
            if (widget.type=='radio') {
                var widget_parent = $(_.str.sprintf("input.%s[type='hidden']", widget.name))[0];
                widget_parent.value = widget.alt;
            }
        },
        evaluate_conditions:function() {
            var node_conditions = this.questionnaire.get('node_conditions');
            var node_variables = this.questionnaire.get('node_variables');
            var solved_nodes = {};

            // Solve boolean statements
            for (var key in node_conditions) {
                var condition = node_conditions[key];
                var variable_name = node_variables[condition.operated_node_id[0]]
                var input = $(_.str.sprintf(".inp_%s", variable_name))[0];

                if (input == null) {
                    console.log('Ignoring input because ', _.str.sprintf(".inp_%s", variable_name) ,' not found.');
                    continue;
                }
                console.log('Evaluating ', _.str.sprintf(".inp_%s", variable_name));

                var value = input.value.replace(/\r?\n/g, "\\n");
                if (input.type == "checkbox") 
                    value = input.checked;
                if (input.type == "radio") 
                    value = input.checked;

                var not = (condition.operator.indexOf('not') >= 0) && '!' || '';
                var oper = condition.operator.replace(/not /,'');
                var statement = _.str.sprintf("%s('%s' %s %s)", not, value, oper, condition.value);
                console.log(' - Evaluate: ! ', statement)
                var evaluation = !eval(statement);
                console.log(' - Solve: ', evaluation);

                for (var i in condition.node_ids) {
                    var target_variable = node_variables[condition.node_ids[i]];
                    if (!(target_variable in solved_nodes)) {
                        solved_nodes[target_variable] = evaluation;
                    } else {
                        solved_nodes[target_variable] = solved_nodes[target_variable] || evaluation;
                    }
                }
            };
            // Asign state
            for (variable_name in solved_nodes) {
                var controls = $(_.str.sprintf("input[name='inp_%s'],.inp_%s", variable_name, variable_name));
		controls.prop("disabled", solved_nodes[variable_name]);
                if (controls) {
                    console.log("Disabling ", variable_name, " ? ",  solved_nodes[variable_name]);
                } else {
                    console.log("Cant found:",_.str.sprintf(".inp_%s", variable_name));
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
        calc_globals:function(){
            var self = this;
            /* P15 */
	    /* Habilito todo */
            var P16 = $("input").index($("input[class^='inp_P16_']:first"));
            var P23 = $("input").index($("input[class^='inp_P23_']:last"));
	    /*$("input").each(function(index, value) {
		    if (P16 <= index && index <= P23) value.disabled=false;
	    });*/
	    /* 2011 y Actuales : NO -> deshabilitar de 16 a 23 */
	    var cant_P15_NO = $("input[class^='inp_P15_'][value='NO']").length;
            if (cant_P15_NO == 8) {
                var last_P16_idx = $("input").index($("input[class^='inp_P16_']:first"));
                var first_P23_idx = $("input").index($("input[class^='inp_P23_']:last"));
                $("input").each(function(index, value) {
                    if (last_P16_idx <= index && index <= first_P23_idx) {
                        value.disabled=true;
                    };
                });
            }
	    /* 2011 : NO -> deshabilitar 17 a 24 */
            var cant_P15_NO = $("input[class^='inp_P15_2011_'][value='NO']").length;
            if (cant_P15_NO == 4) {
                var last_P17_idx = $("input").index($("input[class^='inp_P17_']:first"));
                var first_P23_idx = $("input").index($("input[class^='inp_P23_']:last"));
                $("input").each(function(index, value) {
                    if (last_P17_idx <= index && index <= first_P23_idx) {
                        value.disabled=true;
                    };
                });
            };
	    /* 2011 : SI -> habilita 16.1 */
            var cant_P15_NO = $("input[class^='inp_P15_2011_'][value='NO']").length;
	    if (cant_P15_NO == 4) {
	    	$("input.inp_P16_1").prop('disabled',true);
	    }
	    /* Actuales : SI -> habilita 16.2 */
            var cant_P15_NO = $("input[class^='inp_P15_ACT_'][value='NO']").length;
	    if (cant_P15_NO == 4) {
		$("input.inp_P16_2").prop('disabled',true);
	    }
            /* Años */
            var year_input = $(".type_year");
            year_input.each(function(index, input) {
                if (input.value != '' && !(1810 <= parseInt(input.value) && parseInt(input.value) <= 2013)) {
                    self.do_warn('Año inválido.', 'El valor debe estar entre 1810 y 2013.');
                    input.style.borderColor = 'red';
                } else {
                    input.style.borderColor = 'lightgray';
                };
            });
            /* Porcentuales */
            var por_input = $(".inp_P10_2011,.inp_P10_ACT,.inp_P16_1,.inp_P16_2,.inp_P23_1,.inp_P23_2,.inp_P23_3,.inp_P23_4,.inp_P23_5,.inp_P23_6,.inp_P23_7,.inp_P23_8,.inp_P23_9");
            por_input.each(function(index, input) {
                if (input.value != '' && !(0 <= parseFloat(input.value) && parseFloat(input.value) <= 100)) {
                    self.do_warn('Porcentaje inválido.', 'El valor debe estar entre 0 y 100.');
                    input.style.borderColor = 'red';
                } else {
                    input.style.borderColor = 'lightgray';
                };
            });
            /* P23: Suma debe dar 100!!! */
            var por_input = $(".inp_P23_1,.inp_P23_2,.inp_P23_3,.inp_P23_4,.inp_P23_5,.inp_P23_6,.inp_P23_7,.inp_P23_8,.inp_P23_9");
            var total = 0;
	    var allval = 0;
            por_input.each(function(index, input) {
                if (input.value != '') {
                    total = total + parseFloat(input.value);
		    allval = allval + 1;
                } else {
			input.value = 0;
		}
	    });
	    $(".inp_P23_TOTAL").prop("value",total);
            if (allval >= 8 && total != 0 && total != 100) {
                self.do_warn('Inválida la pregunta 23.', 'La suma de las proporciones debe ser igual a 100%. Actualmente suma: ' + total);
                $(".inp_P23_TOTAL").css({borderColor:'red'});
            } else {
                $(".inp_P23_TOTAL").css({borderColor:'lightgray'});
            };
            /* P26: No puede asignarse una misma opción a cada afirmación */
            var opt_input = $(".inp_P26_1,.inp_P26_2,.inp_P26_3");
            var s = 0;
            var in_range = true;
	    var has_value = true;
            opt_input.each(function(index, input) {
		    var v = parseInt(input.value,10)
		    s = s + v;
		    in_range = in_range && 1 <= v && v <= 3 ;
		    has_value = has_value && !isNaN(v);
	    });
	    if (has_value && !(in_range && s == 6)) {
		    self.do_warn('Pregunta 26', 'Respuesta incorrecta');
	    }

	    /* P14: suma */
	    var s = 0;
	    S = $('.inp_P14_1_AL31,.inp_P14_2_AL31,.inp_P14_3_AL31,.inp_P14_4_AL31');
	    S.each(function(index, item){s = s + (parseInt(item.value,10) || 0);});
	    $('.inp_P14_5_AL31')[0].value = s || 0;
            if (s > 250) {
		    self.do_warn('Pregunta 14', 'El total de ocupados no puede superar los 250.');
                    $('.inp_P14_5_AL31').css({borderColor:'red'});
            } else {
                    $('.inp_P14_5_AL31').css({borderColor:'lightgray'});
            }
	    var s = 0;
	    S = $('.inp_P14_1_ACT,.inp_P14_2_ACT,.inp_P14_3_ACT,.inp_P14_4_ACT');
	    S.each(function(index, item){s = s + (parseInt(item.value,10) || 0);});
	    $('.inp_P14_5_ACT')[0].value = s || 0;
            if (s > 250) {
		    self.do_warn('Pregunta 14', 'El total de ocupados no puede superar los 250.');
                    $('.inp_P14_5_ACT').css({borderColor:'red'});
            } else {
                    $('.inp_P14_5_ACT').css({borderColor:'lightgray'});
            }
            
            /* P20.1: total <= 250 */
            var s = parseInt($('.inp_P20_CANT')[0].value);
            if (!isNaN(s) && s > 250) {
		    self.do_warn('Pregunta 20.1', 'El total de personas no puede superar los 250.');
                    $('.inp_P20_CANT').css({borderColor:'red'});
            } else {
                    $('.inp_P20_CANT').css({borderColor:'lightgray'});
            }

            /* P8: control de evaluacion */
            var to_enable=$("input[alt='6'][name='inp_P8_ACT'],input[alt='6'][name='inp_P8_2011']");
            var to_check=$("input.inp_P8_1_ESP")
            var r = true;
            to_check.each(function(index, value) { r = r && (value.value==''); });
            if (r) to_enable.prop('disabled', true);
        },
    })

};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
