var table = {}
        $(document).ready(function () {
            table = $("#my_books").DataTable( {
                responsive: true,
                iDisplayLength: -1,
                columnDefs: [
                { orderable: false, targets: 0 },
                // { orderDataType: "dom-text", type: "string", targets: 1 },
                // { orderDataType: "dom-text", type: "string", targets: 3 }
                ],
                order: [[1, "asc"]],

                language: {
                    "decimal":        "",
                    "emptyTable":     "",
                    "info":           "Zobrazeno _START_ až _END_ z _TOTAL_ výsledků",
                    "infoEmpty":      "Zobrazeno 0 výsledků",
                    "infoFiltered":   "(filtrováno z _MAX_ total výsledků)",
                    "infoPostFix":    "",
                    "thousands":      ",",
                    "lengthMenu":     "Zobrazit _MENU_ výsledků",
                    "loadingRecords": "Načítám...",
                    "processing":     "",
                    "search":         "Vyhledat:",
                    "zeroRecords":    "",
                    "paginate": {
                        "first":      "První",
                        "last":       "Poslední",
                        "next":       "Další",
                        "previous":   "Předchozí"
                        }
                    }
                } );
            });
            $("#my_books").on('draw.dt', function(){
                let n = 0;
                $(".number").each(function () {
                        $(this).html(++n + ".");
            });
        });

        $(".change-input-title").focus(function () {
            $(this).addClass("large_input");
        });
        $(".change-input-title").blur(function () {
            $(this).removeClass("large_input");
        });
        $(".change-input-author").focus(function () {
            $(this).addClass("medium_input");
        });
        $(".change-input-author").blur(function () {
            $(this).removeClass("medium_input");
        });