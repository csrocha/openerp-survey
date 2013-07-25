// static/src/js/widgets.js
function openerp_zondaggio_models(instance, module){
    var QWeb = instance.web.qweb;

    module.Questionnaire = Backbone.Model.extend({
        initialize: function(session,attributes){
            Backbone.Model.prototype.initialize.call(this, attributes);
            var self = this;
            this.session = session;
            this.ready = $.Deferred();                          // used to notify the GUI that the PosModel has loaded all resources
            this.flush_mutex = new $.Mutex();                   // used to make sure the orders are sent to the server once at time
            this.active_id = session.questionnaire_context.active_id || session.questionnaire_params.active_id;

            if (this.active_id == null) {
                return self.ready.reject();
            };

            this.set({
                'questionnaire': null,
                'survey': null,
                'nodes': [],
                'pages': [],
                'tree': {},
                'root': null,
            });

            $.when(this.load_server_data())
                .done(function(){
                    self.ready.resolve();
                }).fail(function(){
                    self.ready.reject();
                });
        },
        // helper function to load data from the server
        fetch: function(model, fields, domain, ctx){
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },
        // loads all the needed data on the sever. returns a deferred indicating when all the data has loaded. 
        load_server_data: function(){
            var self = this;

            var loaded = self.fetch('sondaggio.category', ['name'],[])
                .then(function(categories){
                    map_classes={}
                    map_widgets={}
                    categories.forEach(function(cat){
                        if (cat.name.indexOf('zoe_') == 0) { map_classes[cat.id]=cat.name; }
                        if (cat.name.indexOf('widget_') == 0) { map_widgets[cat.id]=cat.name; }
                    });
                    self.set('classes', map_classes);
                    self.set('widgets', map_widgets);
            
                    return self.fetch('sondaggio.questionnaire',['name','description','survey_id'],[['id','=',self.active_id]]);        
                }).then(function(questionnaires){
                    self.set('questionnaire',questionnaires[0]);

                    return self.fetch('sondaggio.survey',['name','description'],[['id','=',questionnaires[0].survey_id[0]]]);
                }).then(function(surveys){
                    self.set('survey',surveys[0]);

                    return self.fetch('sondaggio.node',[
                        'name','question','type','initial_state',
                        'page','complete_place',
                        'enable_in','format_id','parent_id',
                        'category_ids','enable_condition_ids',
                        'child_ids',
                        ],[['survey_id','=',surveys[0].id]]);
                }).then(function(nodes){
                    // Group by pages
                    pages = {};
                    nodes.forEach(function(node){
                        if (!(node.page in pages)) { pages[node.page] = []; };
                        pages[node.page].push(node);
                    })
                    // Set categories as classes & widgets
                    classes = self.get('classes')
                    widgets = self.get('widgets')
                    nodes.forEach(function(node){
                        node_classes = [];
                        node_widgets = [];
                        node.category_ids.forEach(function(cat){
                            if (cat in classes) { node_classes.push(classes[cat]); }
                            if (cat in widgets) { node_widgets.push(widgets[cat]); }
                        });
                        node.classes = node_classes.join(' ');
                        node.widget = node_widgets[0] || null;
                    });
                    // Set node_ids & node_complete_place
                    node_ids = [];
                    node_complete_places = {}
                    complete_place_nodes = {}
                    nodes.forEach(function(node){
                        node_ids.push(node.id);
                        node_complete_places[node.id] = node.complete_place;
                        complete_place_nodes[node.complete_place] = node.id;
                    });
                    // Set herarchical tree topology
                    var tree = {};
                    var root = null;
                    var node_dict = {};
                    nodes.forEach(function(node){
                        tree[node.id] = node.child_ids;
                        if (node.parent_id == false) {
                            root = node.id;
                        };
                        node_dict[node.id] = node;
                    });

                    // Save variables
                    self.set('pages',pages);
                    self.set('nodes',nodes);
                    self.set('node_dict',node_dict);
                    self.set('tree',tree);
                    self.set('root',root);
                    self.set('node_complete_places',node_complete_places);
                    self.set('complete_place_nodes',complete_place_nodes);

                    // Take restrictions
                    return self.fetch('sondaggio.enable_condition',['node_id','operated_node_id','operator','value'],[['node_id','in',node_ids]]);
                }).then(function(conditions){
                    node_conditions = {};
                    conditions.forEach(function(condition){
                        if (!(condition.node_id[0] in node_conditions)) {
                            node_conditions[condition.node_id[0]]=[];
                        }
                        node_conditions[condition.node_id[0]].push({
                            node_id: condition.operated_node_id[0],
                            operator: condition.operator,
                            value: condition.value
                        });
                    });
                    self.set('node_conditions',node_conditions);

                    return self.fetch('sondaggio.answer',[
                        'name',
                        'complete_place',
                        'code',
                        'input',
                        'formated',
                        'message',
                        'valid',
                        'state',
                        'question_id',
                        'questionnaire_id'],
                        [['questionnaire_id', '=', self.active_id]]);
                }).then(function(answers){
                    answer_map = {};
                    for (index in answers) {
                        var answer = answers[index]; 
                        answer_map[answer.question_id[0]] = answer;
                    };
                    self.set('answers', answer_map);
                });
            return loaded;
        },
        save_server_data:function(data){
            return new instance.web.Model('sondaggio.questionnaire').call('write', [[this.active_id], data]);
        },
    });
};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
