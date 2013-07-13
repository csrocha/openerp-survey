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
            this.active_id = session.questionnaire_context.active_id

            if (this.active_id == null) {
                return self.ready.reject();
            };

            this.set({
                'questionnaire': null,
                'survey': null,
                'nodes': [],
                'pages': [],
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
                    map_categories={}
                    categories.forEach(function(cat){
                        if (cat.name.indexOf('zoe_') == 0) {
                            map_categories[cat.id]=cat.name;
                        }
                    });
                    self.set('categories', map_categories);
            
                    return self.fetch('sondaggio.questionnaire',['name','description','survey_id'],[['id','=',self.active_id]]);        
                }).then(function(questionnaires){
                    self.set('questionnaire',questionnaires[0]);

                    return self.fetch('sondaggio.survey',['name','description'],[['id','=',questionnaires[0].survey_id[0]]]);
                }).then(function(surveys){
                    self.set('survey',surveys[0]);

                    return self.fetch('sondaggio.node',['name','question','type','initial_state','page','enable_in','format_id','parent_id','category_ids.name'],[['survey_id','=',surveys[0].id]]);
                }).then(function(nodes){
                    // Group by pages
                    pages = {};
                    nodes.forEach(function(node){
                        if (!(node.page in pages)) { pages[node.page] = []; };
                        pages[node.page].push(node);
                    })
                    self.set('pages',pages);
                    self.set('nodes',nodes);
                });
            return loaded;
        },
    });
};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
