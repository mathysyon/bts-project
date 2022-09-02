<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <!--<meta http-equiv="refresh" content="60"> Refresh automatique toutes les 5 secondes-->
    <title>ConceptBall graphique</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
    <div style="width: 50%">
    <canvas id="graphiqueConceptball"></canvas>
    </div>

    <script>
        var ctx = document.getElementById('graphiqueConceptball').getContext('2d');

        var chart = new Chart(ctx, {
            //The Type of chart we want to create
            type: 'line',

            //The data for our dataset
            data: {
                labels: {{ labels }}, //Récupère "labels" de app.py -> Date et heure
                datasets: [{
                    label: 'Température (°C)',
                    backgroundColor: 'rgba(255, 99, 132, 0.25)',
                    borderColor: 'rgb(255, 0, 0)',
                    data: {{ data }}, //Récupère "data" de app.py -> Valeurs
                }]
            },

            //Configuration options go here
            options: {
                plugins:{
                    title: {
                        display : true, //Affiche le titre
                        text: "Evolution des températures" //Titre du graphique
                    }
                }
                /*scales: {
                    Temp: {
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Température (en °C)'
                        }
                    },
                    Time: {
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Temps'
                        }
                    }
                }*/
            }
        });
    </script>
</body>

</html>