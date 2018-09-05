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
                field: "FileName", title: "File Name", template:function(t) {
                        return'<a class="m-link popovers" data-toggle="popover" href="/result?id='+t.ID+'">'+t.FileName+"</a>"
                    }
            }
             , {
                field:"FileSize", title:"File Size", width: 60
            }, {
                field:"Status", title:"Status", width: 130, template:function(t) {
                    var e= {
                        1: {
                            title: "Validated", class: "m-badge--brand"
                        }
                        , 2: {
                            title: "Validation Error", class: " m-badge--warning"
                        }
                        , 3: {
                            title: "Unvalidated", class: " m-badge--danger"
                        }
                    }
                    ;
                    return'<span class="m-badge '+e[t.Status].class+' m-badge--wide">'+e[t.Status].title+"</span>"
                }
            }
            ]
        }
        ),
        e=t.getDataSourceQuery()

    }
}

;
jQuery(document).ready(function() {
    DatatableJsonRemoteDemo.init()
}

);