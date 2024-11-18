<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Gestion des données</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .single-item p { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Données de la table <?php echo ucfirst($table); ?></h1>
    
    <?php if (is_array($data) && !empty($data)): ?>
        <table>
            <thead>
                <tr>
                    <?php
                    $methods = get_class_methods($data[0]);
                    foreach ($methods as $method) {
                        if (strpos($method, 'get') === 0) {
                            $header = substr($method, 3);
                            echo "<th>" . ucfirst($header) . "</th>";
                        }
                    }
                    ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($data as $row): ?>
                    <tr>
                        <?php
                        foreach ($methods as $method) {
                            if (strpos($method, 'get') === 0) {
                                echo "<td>" . htmlspecialchars($row->$method()) . "</td>";
                            }
                        }
                        ?>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php elseif ($data): ?>
        <div class="single-item">
            <?php
            $methods = get_class_methods($data);
            foreach ($methods as $method) {
                if (strpos($method, 'get') === 0) {
                    $label = substr($method, 3);
                    echo "<p><strong>" . ucfirst($label) . ":</strong> " . htmlspecialchars($data->$method()) . "</p>";
                }
            }
            ?>
        </div>
    <?php else: ?>
        <p>Aucune donnée trouvée.</p>
    <?php endif; ?>
</body>
</html>