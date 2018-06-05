var DatatableJsonRemoteDemo= {
    init:function() {
        var t,
        e;
        t=$(".m_datatable").mDatatable( {
            data: {
                type: "remote", source: "/histories", pageSize: 20
            }
            , layout: {
                theme: "default", class: "", scroll: !1, footer: !1
            }
            , sortable:!0, pagination:!0, search: {
                input: $("#generalSearch")
            }
            , columns:[ {
                field: "ID", title: "#", width: 30, sortable: !1, selector: !1, textAlign: "center"
            }
            , {
                field: "DateUploaded", title: "Date", type: "date", template:function(t) {
                        return moment(t.DateUploaded).format("LLL")
                    }
            }
             , {
                field: "FileName", title: "File Name", width: 210, template:function(t) {
                        return'<a class="m-link popovers" data-toggle="popover" href="/result?id='+t.ID+'">'+t.FileName+"</a>"
                    }
            }
             , {
                field:"FileSize", title:"File Size", width: 60
            }
            , {
                field:"Type", title:"Type", width: 60 , template:function(t) {
                    var e= {
                        'bb': {
                            title: "Building Block", state: "accent"
                        }
                        , 'sc': {
                            title: "Screening Compounds", state: "info"
                        }
                        , 'both': {
                            title: "Mixed", state: "focus"
                        }
                    }
                    ;
                    return'<span class="m--font-bold m--font-'+e[t.Type].state+'">'+e[t.Type].title+"</span>"
                }
            }
            , {
                field:"Purchasability", title:"Purchasability", width: 50, template:function(t) {
                    var e= {
                        'stock': {
                            title: "In Stock", class: " m--font-primary"
                        }
                        , 'demand': {
                            title: "Make on Demand", class: " m--font-accent"
                        }
                    }
                    ;
                    return'<span class="m--font-bold '+e[t.Purchasability].class+' m-badge--wide">'+e[t.Purchasability].title+"</span>"
                }
            }
            , {
                field:"NaturalProducts", title:"Natural Products", width: 50
            }
            , {
                field:"Status", title:"Status", template:function(t) {
                    var e= {
                        1: {
                            title: "Job Submitted", class: "m-badge--brand"
                        }
                        , 2: {
                            title: "Warning", class: " m-badge--warning"
                        }
                        , 3: {
                            title: "Error", class: " m-badge--danger"
                        }
                        , 4: {
                            title: "Job Finished", class: " m-badge--success"
                        }
                    }
                    ;
                    return'<span class="m-badge '+e[t.Status].class+' m-badge--wide">'+e[t.Status].title+"</span>"
                }
            }
            ]
        }
        ),
        e=t.getDataSourceQuery(),
        $("#m_form_status").on("change", function() {
            t.search($(this).val(), "Status")
        }
        ).val(void 0!==e.Status?e.Status:""),
        $("#m_form_type").on("change", function() {
            t.search($(this).val(), "Type")
        }
        ).val(void 0!==e.Type?e.Type:""),
        $("#m_form_status, #m_form_type").selectpicker()
    }
}

;
jQuery(document).ready(function() {
    DatatableJsonRemoteDemo.init()
}

);