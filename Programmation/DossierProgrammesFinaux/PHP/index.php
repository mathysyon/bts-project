<?php
    $host = 'localhost';
    $user = 'root';
    $pass = 'conceptball';
    $db = 'releve_conceptball';
    $mysqli = new mysqli($host,$user,$pass,$db) or die($mysqli->error);

    $dataTempValue = '';
    $dataTempTime = '';

    $sql = "SELECT * FROM Releve WHERE c_id_Capteur= 4 ORDER BY r_dateheure_Releve DESC LIMIT 5";
    //print(array_reverse($sql));
    $result = mysqli_query($mysqli, $sql);

    while ($row = mysqli_fetch_array($result)) {

		$dataTempValue = $dataTempValue . '"'. $row['r_valeur_Releve'].'",';
        $dataTempTime = $dataTempTime . '"'. $row['r_dateheure_Releve'].'",';
	}

	$dataTempValue = trim($dataTempValue,","); //data1
    $dataTempTime = trim($dataTempTime,","); //data2
?>


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
                labels: [<?php echo $dataTempTime; ?>], 
                datasets: [{
                    label: 'Température (°C)',
                    backgroundColor: 'rgba(255, 99, 132, 0.25)',
                    borderColor: 'rgb(255, 0, 0)',
                    data: [<?php echo $dataTempValue; ?>],
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