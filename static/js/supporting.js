(function (document) {
    'use strict';

    var LightTableSorter = (function (Arr) {

        var _th, _cellIndex, _order = '';

        function _text(row) {
            return row.cells.item(_cellIndex).textContent.toLowerCase();
        }

        function _sort(a, b) {
            var va = _text(a), vb = _text(b), n = parseInt(va, 10);
            if (n) {
                va = n;
                vb = parseInt(vb, 10);
            }
            return va > vb ? 1 : va < vb ? -1 : 0;
        }

        function _toggle() {
            var c = _order !== 'asc' ? 'asc' : 'desc';
            _th.className = (_th.className.replace(_order, '') + ' ' + c).trim();
            _order = c;
        }

        function _reset() {
            _th.className = _th.className.replace('asc', '').replace('desc', '');
            _order = '';
        }

        function onClickEvent(e) {
            if (_th && _cellIndex !== e.target.cellIndex) {
                _reset();
            }
            _th = e.target;
            _cellIndex = _th.cellIndex;
            var tbody = _th.offsetParent.getElementsByTagName('tbody')[0],
                rows = tbody.rows;
            if (rows) {
                rows = Arr.sort.call(Arr.slice.call(rows, 0), _sort);
                if (_order === 'asc') {
                    Arr.reverse.call(rows);
                }
                _toggle();
                tbody.innerHtml = '';
                Arr.forEach.call(rows, function (row) {
                    tbody.appendChild(row);
                });
            }
        }

        return {
            init: function () {
                var ths = document.getElementsByTagName('th');
                Arr.forEach.call(ths, function (th) {
                    th.onclick = onClickEvent;
                });
            }
        };
    })(Array.prototype);

    document.addEventListener('readystatechange', function () {
        if (document.readyState === 'complete') {
            LightTableSorter.init();
        }
    });

})(document);

$(document).ready(function () {
    var activeSystemClass = $('.list-group-item.active');

    //something is entered in search form
    $('#system-search').keyup(function () {
        var that = this;
        // affect all table rows on in systems table
        var tableBody = $('.table-list-search tbody');
        var tableRowsClass = $('.table-list-search tbody tr');
        $('.search-sf').remove();
        tableRowsClass.each(function (i, val) {

            //Lower text for case insensitive
            var rowText = $(val).text().toLowerCase();
            var inputText = $(that).val().toLowerCase();
            if (inputText != '') {
                $('.search-query-sf').remove();
                tableBody.prepend('<tr class="search-query-sf"><td colspan="8"><strong>Buscando por: "'
                    + $(that).val()
                    + '"</strong></td></tr>');
            }
            else {
                $('.search-query-sf').remove();
            }

            if (rowText.indexOf(inputText) == -1) {
                //hide rows
                tableRowsClass.eq(i).hide();

            }
            else {
                $('.search-sf').remove();
                tableRowsClass.eq(i).show();
            }
        });
        //all tr elements are hidden
        if (tableRowsClass.children(':visible').length == 0) {
            tableBody.append('<tr class="search-sf"><td class="text-muted" colspan="8">No hay coincidencias.</td></tr>');
        }
    });
});

