// ATTENTION: Ne commitez JAMAIS votre clé API dans ce fichier!
// Utilisez une des méthodes suivantes:
// 1. Variable d'environnement: const String openWeatherMapApiKey = String.fromEnvironment('OPENWEATHERMAP_API_KEY');
// 2. Fichier .env avec flutter_dotenv (voir config.example.dart)
// 3. Passer via --dart-define lors du build: flutter run --dart-define=OPENWEATHERMAP_API_KEY=your_key

// Pour le développement local, créez un fichier config.local.dart (non versionné)
// et importez-le à la place de config.dart dans main.dart

const String openWeatherMapApiKey = String.fromEnvironment(
  'OPENWEATHERMAP_API_KEY',
  defaultValue: '', // Ne pas mettre de clé par défaut ici!
);