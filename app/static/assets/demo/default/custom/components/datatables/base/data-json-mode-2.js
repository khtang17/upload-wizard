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