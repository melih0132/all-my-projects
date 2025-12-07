// Fichier d'exemple - Copiez ce fichier vers config.dart et ajoutez votre clé API
// Pour utiliser des variables d'environnement, utilisez le package flutter_dotenv
// ou passez la clé via les arguments de build

// Option 1: Variable d'environnement (recommandé)
// const String openWeatherMapApiKey = String.fromEnvironment(
//   'OPENWEATHERMAP_API_KEY',
//   defaultValue: '',
// );

// Option 2: Fichier .env avec flutter_dotenv (recommandé pour le développement)
// import 'package:flutter_dotenv/flutter_dotenv.dart';
// final String openWeatherMapApiKey = dotenv.env['OPENWEATHERMAP_API_KEY'] ?? '';

// Option 3: Placeholder (à remplacer)
const String openWeatherMapApiKey = 'YOUR_OPENWEATHERMAP_API_KEY_HERE';

