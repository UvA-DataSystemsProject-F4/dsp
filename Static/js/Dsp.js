function toDataTable(id) {
    $("#" + id).DataTable({
        aaSorting: [],
        paging: true,
        pagingType: "simple_numbers",
        pageLength: 25,
        scrollX: true,
        sScrollX: "100%",
    });
}

function redirectTo(id) {
    window.location = id
}

function redirectToNewTab(id) {
    window.open(id, '_blank')
}


class Helpers {
    static RandomColor() {
        return Math.floor(Math.random() * 16777215).toString(16);
    }
}

class Charts {
    static CreateLoadingElement(id) {
        return "<div id='loading_" + id + "' class=\"text-center\">\n" +
            "    <span>Loading data... Please wait...</span><br>\n" +
            "  <div class=\"spinner-border text-primary\" role=\"status\">\n" +
            "    <span class=\"visually-hidden\">Loading...</span>\n" +
            "  </div>\n" +
            "</div>"
    }

    static CreateErrorPane(msg) {
        return "<div class=\"text-center\">\n" +
            "<i class=\"fas fa-times fa-2x\" style='color: #d9534f'><br>ERROR</i><br>\n" +
            "<span>" + msg + "<span><br>\n" +
            "</div>"
    }

    static CreateLineStyle() {
        return {
            fill: false,
            borderColor: "#" + Helpers.RandomColor(),
            tension: 0.2
        }
    }

    static CreateScatterStyle() {
        return {
            backgroundColor: "#" + Helpers.RandomColor(),
        }
    }

    static CreateBarChartStyle(items) {
        var colors = []
        for (let i = 0; i < items; i++) {
            colors.push("#2b2b2b")
        }
        return {
            backgroundColor: colors
        }
    }


    static CreateBarChart(cid, data_url, parameters) {
        const container = document.getElementById(cid).parentElement
        container.innerHTML = this.CreateLoadingElement()
        console.log(data_url)
        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
            url: data_url,
            data: parameters,
            success: function (response) {
                const canvas = document.createElement('canvas');
                canvas.id = cid
                container.innerHTML = canvas.outerHTML
                const ctx = document.getElementById(cid).getContext('2d');

                for (let i = response['datasets'].length - 1; i >= 0; i--) {
                    $.extend(response['datasets'][i], Charts.CreateBarChartStyle(response['datasets'][i]['data'].length));
                }
                new Chart(ctx, {
                    options: {
                        maintainAspectRatio: false,
                        onClick: (e) => {
                            const points = e.chart.getElementsAtEventForMode(e, 'nearest', {intersect: true}, true);
                            if (points.length) {
                                const label = e.chart.data.labels[points[0].index];
                                showDetailModal(label)
                            }
                        }
                    },
                    type: 'bar',
                    data: response
                });
            },
            error: function (response) {
                container.innerHTML = Charts.CreateErrorPane(response.responseText)
            },
        });
    }

    static CreateScatterChart(cid, data_url, parameters) {
        const container = document.getElementById(cid).parentElement
        container.innerHTML = this.CreateLoadingElement()
        console.log(data_url)
        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
            url: data_url,
            data: parameters,
            success: function (response) {
                const canvas = document.createElement('canvas');
                canvas.id = cid
                container.innerHTML = canvas.outerHTML
                const ctx = document.getElementById(cid).getContext('2d');
                for (let i = response['datasets'].length - 1; i >= 0; i--) {
                    $.extend(response['datasets'][i], Charts.CreateScatterStyle());
                }
                new Chart(ctx, {
                    options: {
                        maintainAspectRatio: false,
                    },
                    type: 'scatter',
                    data: response
                });
            },
            error: function (response) {
                container.innerHTML = Charts.CreateErrorPane(response.responseText)
            },
        });
    }
}

