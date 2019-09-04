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
                field:"CatalogType", title:"Catalog Type", width: 60 , template:function(t) {
                    var e= {
                        'bb': {
                            title: "Building Block", state: "accent", icon : "leaf"
                        }
                        , 'sc': {
                            title: "Screening Compounds", state: "info", icon : "times"
                        }
                        , 'both': {
                            title: "Mixed", state: "focus", icon : "times"
                        }
                        , 'np': {
                            title: "Natural Product", state: "focus", icon : "leaf"
                        }
                        , 'bio': {
                            title: "Bioactives", state: "focus", icon : "times"
                        }
                    }
                    ;
                     return'<span class="m--font-bold m--font-'+e[t.CatalogType].state+'"><i class="fa fa-'+ e[t.CatalogType.icon]+' fa-5x"></i>'+e[t.CatalogType].title+"</span>"
                }
            },
             {
                field:"UploadType", title:"Upload Type", width: 60 , template:function(t) {
                    var e= {
                        'full': {
                            title: "Full Update", state: "accent"
                        }
                        , 'incremental': {
                            title: "Incremental Update", state: "info"
                        }
                    }
                    ;
                    return'<span class="m--font-bold m--font-'+e[t.UploadType].state+'">'+e[t.UploadType].title+"</span>"
                }
            },

            {
                field:"Availability", title:"Availability", width: 80, template:function(t) {
                    var e= {
                        'stock': {
                            title: "In Stock", class: " m--font-primary"
                        }
                        , 'demand': {
                            title: "Make on Demand", class: " m--font-accent"
                        }
                    }
                    ;
                    return'<span class="m--font-bold '+e[t.Availability].class+' m-badge--wide">'+e[t.Availability].title+"</span>"
                }
            }
            , {
                field:"StatusId", title:"Status ID", template:function(t) {
                    var e= {
                        1: {
                            title: "File Submitted", class: "m-badge--brand"
                        }
                        , 2: {
                            title: "Validation Started", class: "m-badge--brand"
                        }
                        , 3: {
                            title: "Validation Failed", class: " m-badge--danger"
                        }
                        , 4: {
                            title: "Validation Completed", class: " m-badge--brand"
                        }
                        , 5: {
                            title: "Prepare for Loading", class: "m-badge--warn"
                        }
                        , 6: {
                            title: "Fail to Prepare for Loading", class: "m-badge--danger"
                        }
                        , 7: {
                            title: "Loading Started", class: "m-badge--brand"
                        }
                        , 8: {
                            title: "Loading Completed", class: "m-badge--brand"
                        }
                        , 9: {
                            title: "Loading Failed", class: "m-badge--danger"
                        }
                        , 10: {
                            title: "Depletion", class: "m-badge--brand"
                        }
                        , 11: {
                            title: "Finished", class: " m-badge--success"
                        }
                        , 12: {
                            title: "Awaiting System Admin Review", class: "m-badge--warn"
                        }
                        , 13: {
                            title: "Job Cancelled by Admin", class: "m-badge--danger"
                        }
                        , 14: {
                            title: "Job Cancelled by System", class: "m-badge--danger"
                        }
                        , 15: {
                            title: " Admin Attention: Pricing specified", class: "m-badge--warn"
                        }

                    }
                    ;
                    return'<span class="m-badge '+e[t.StatusId].class+' m-badge--wide">'+e[t.StatusId].title+"</span>"
                }
            }
            ]
        }
        ),
        e=t.getDataSourceQuery(),
        $("#m_form_status").on("change", function() {
            t.search($(this).val(), "StatusId")
        }
        ).val(void 0!==e.StatusId?e.StatusId:""),
        $("#m_form_type").on("change", function() {
            t.search($(this).val(), "CatalogType")
        }
        ).val(void 0!==e.CatalogType?e.CatalogType:""),
        $("#m_form_status, #m_form_type").selectpicker()
    }
}

;
jQuery(document).ready(function() {
    DatatableJsonRemoteDemo.init()
}

);