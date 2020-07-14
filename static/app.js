$(document).ready(function () {
    fetch('http://localhost:5000/api/v1/products')
        .then(response => {
            return response.json()
        })
        .then(data => {
            let result = []
            console.log(data)
            data.map(item => {
                result.push([
                    item.name,
                    item.image[0],
                    item.brand.name,
                    item.url,
                    item.sku,
                    item.ean,
                    item.offers.lowPrice,
                    item.offers.highPrice,
                ])
            })

            return result
        })
        .then(data => {
            var tabela = $("#table").DataTable({
                "data": data,
                "columns": [
                    {'data': 0},
                    {
                        "render": (data, type, full, meta) => {
                            return '<img src="' + data + '" />'
                        }
                    },
                    {'data': 2},
                    {
                        'data': 3, "render": (data, type, full, meta) => {
                            return '<a href="' + data + '" target="_blank">Acessar página</a>'
                        }
                    },
                    {'data': 4},
                    {'data': 5},
                    {'data': 6},
                    {'data': 7},
                ]
            })
        })
})
