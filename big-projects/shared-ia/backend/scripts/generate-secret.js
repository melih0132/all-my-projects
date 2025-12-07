import crypto from 'crypto';

// Générer une clé secrète aléatoire de 32 bytes en base64
const secret = crypto.randomBytes(32).toString('base64');

console.log('\nCle secrete JWT generee :\n');
console.log(secret);
console.log('\nCopiez cette cle dans votre fichier .env comme valeur de JWT_SECRET\n');

