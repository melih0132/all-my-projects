using System;
using System.IO;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Windows.Threading;
using System.Reflection;

namespace NinjaJeu
{
    public partial class MainWindow : Window
    {
        private int score = 0;
        private int vie = 3;
        private int niveau = 1;
        private int vieRestant;
        private bool vieAjoutee = false;
        private int vitesseShuriken = 10;

        private bool augmentationFaite = false;
        private bool modeInvincible = false;
        private bool pause = false;
        private bool gauche = false;
        private bool droite = false;

        string assemblyName = Assembly.GetExecutingAssembly().GetName().Name;

        private SpriteAnimation idleAnimation;
        private SpriteAnimation runAnimation;
        private SpriteAnimation runLeftAnimation;
        private SpriteAnimation attackAnimation;
        private SpriteAnimation hurtAnimation;
        private bool isHurt;

        public static MediaPlayer musiqueDeFond = new MediaPlayer();
        DispatcherTimer minuterie = new DispatcherTimer();
        List<Rectangle> listeShuriken = new List<Rectangle>();
        List<Rectangle> listePowerUps = new List<Rectangle>();
        Random aleatoire = new Random();

        public MainWindow()
        {
            InitializeComponent();

            InitializeAnimations();
            PersoRect.RenderTransform = new ScaleTransform(1.75, 1.75);

            musiqueDeFond.Open(new Uri("SonFond.mp3", UriKind.Relative));
            musiqueDeFond.Volume = 0.1;
            musiqueDeFond.Play();

            EntreeEnJeu entreeEnJeu = new EntreeEnJeu();
            entreeEnJeu.ShowDialog();

            if (entreeEnJeu.DialogResult == true)
            {
                CreerShurikens();
            }

            InitialiserJeu();
        }

        private void InitializeAnimations()
        {
            ImageBrush persoBrush = (ImageBrush)PersoRect.Fill;

            idleAnimation = new SpriteAnimation(persoBrush,
                $"pack://application:,,,/{assemblyName};component/Sprites/IDLE.png",
                frameWidth: 96,
                frameHeight: 96,
                frameCount: 10,
                fps: 8);

            runAnimation = new SpriteAnimation(persoBrush,
                $"pack://application:,,,/{assemblyName};component/Sprites/RUN.png",
                frameWidth: 96,
                frameHeight: 96,
                frameCount: 16,
                fps: 12);

            runLeftAnimation = new SpriteAnimation(persoBrush,
                $"pack://application:,,,/{assemblyName};component/Sprites/RUN_LEFT.png",
                frameWidth: 96,
                frameHeight: 96,
                frameCount: 16,
                fps: 12);

            attackAnimation = new SpriteAnimation(persoBrush,
                $"pack://application:,,,/{assemblyName};component/Sprites/ATTACK.png",
                frameWidth: 96,
                frameHeight: 96,
                frameCount: 7,
                fps: 10);

            hurtAnimation = new SpriteAnimation(persoBrush,
                $"pack://application:,,,/{assemblyName};component/Sprites/HURT.png",
                frameWidth: 96,
                frameHeight: 96,
                frameCount: 4,
                fps: 6);

            var firstFrame = new CroppedBitmap(
                new BitmapImage(new Uri($"pack://application:,,,/{assemblyName};component/Sprites/IDLE.png", UriKind.Absolute)),
                new Int32Rect(0, 0, 96, 96));
            persoBrush.ImageSource = firstFrame;
        }

        public static void GerermusiqueDeFond()
        {
            musiqueDeFond.IsMuted = !musiqueDeFond.IsMuted;
        }

        public static bool RenvoieTrueSimusiqueDeFondDesactive()
        {
            return musiqueDeFond.IsMuted;
        }

        public void Rejouer()
        {
            minuterie.Stop();
            minuterie.Tick -= BoucleJeu;

            foreach (Rectangle shuriken in listeShuriken)
            {
                if (JeuCanva.Children.Contains(shuriken))
                {
                    JeuCanva.Children.Remove(shuriken);
                }
            }
            listeShuriken.Clear();

            foreach (Rectangle powerUp in listePowerUps)
            {
                if (JeuCanva.Children.Contains(powerUp))
                {
                    JeuCanva.Children.Remove(powerUp);
                }
            }
            listePowerUps.Clear();

            InitialiserJeu();
        }

        private void InitialiserJeu()
        {
            score = 0;
            vieRestant = vie;
            vitesseShuriken = 10;
            modeInvincible = false;
            pause = false;
            gauche = false;
            droite = false;
            augmentationFaite = false;

            minuterie.Interval = TimeSpan.FromMilliseconds(16);
            minuterie.Start();

            minuterie.Tick += BoucleJeu;

            KeyDown -= Window_KeyDown;
            KeyDown += Window_KeyDown;
            KeyUp -= Window_KeyUp;
            KeyUp += Window_KeyUp;

            CreerShurikens();
            CreerPowerUp();

            AfficherScoreEtVie(score, vieRestant);
        }

        private void BoucleJeu(object sender, EventArgs e)
        {
            if (pause)
            {
                return;
            }

            GestionModifVitesseShuriken();
            AjouterVie();
            CreerPowerUp();

            foreach (Rectangle shuriken in listeShuriken)
            {
                DeplacerShuriken(shuriken);
                AfficherScoreEtVie(score, vieRestant);
                if (CollisionAvecNinja(shuriken))
                {
                    if (!modeInvincible)
                    {
                        isHurt = true;
                        runAnimation.Stop();
                        idleAnimation.Stop();
                        hurtAnimation.Start();

                        DispatcherTimer hurtTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(0.5) };
                        hurtTimer.Tick += (s, e) =>
                        {
                            isHurt = false;
                            hurtAnimation.Stop();
                            hurtTimer.Stop();
                            idleAnimation.Start();
                        };
                        hurtTimer.Start();

                        vieRestant--;
                        AnimerCollision(shuriken);
                        ReinitialiserPositionShuriken(shuriken);
                    }

                    if (vieRestant <= 0)
                    {
                        FinDuJeu();
                        return;
                    }
                }
            }

            foreach (Rectangle powerUp in listePowerUps)
            {
                DeplacerPowerUp(powerUp);
                if (CollisionAvecNinja(powerUp))
                {
                    ActiverInvincible();
                    JeuCanva.Children.Remove(powerUp);
                    listePowerUps.Remove(powerUp);
                    break;
                }
            }

            MouvementNinja();
            NettoyerObjetsInutilises();
        }

        private void AjouterVie()
        {
            if (score % 30 == 0 && score != 0 && !vieAjoutee)
            {
                vieRestant++;
                vieAjoutee = true;
            }
            else if (score % 30 != 0)
            {
                vieAjoutee = false;
            }
        }

        private void GestionModifVitesseShuriken()
        {
            if (score % 10 == 0 && !augmentationFaite && score > 0)
            {
                vitesseShuriken += 2;
                augmentationFaite = true;
                niveau++;
                AfficherNiveau(niveau);
            }
            else if (score % 10 != 0)
            {
                augmentationFaite = false;
            }
        }

        private void AfficherNiveau(int niveau)
        {
            NiveauText.Text = $"Niveau: {niveau}";

            DoubleAnimation animation = new DoubleAnimation
            {
                From = 1.0,
                To = 1.5,
                Duration = new Duration(TimeSpan.FromSeconds(0.3)),
                AutoReverse = true
            };

            ScaleTransform scaleTransform = new ScaleTransform(1, 1);
            NiveauText.RenderTransform = scaleTransform;
            scaleTransform.BeginAnimation(ScaleTransform.ScaleXProperty, animation);
            scaleTransform.BeginAnimation(ScaleTransform.ScaleYProperty, animation);
        }

        private void CreerPowerUp()
        {
            if (score % 20 == 0 && score != 0 && !listePowerUps.Exists(p => Canvas.GetTop(p) == -18))
            {
                Rectangle powerUp = new Rectangle
                {
                    Width = 20,
                    Height = 18,
                    Fill = new SolidColorBrush(Color.FromRgb(255, 255, 0))
                };

                Canvas.SetTop(powerUp, -18);
                Canvas.SetLeft(powerUp, aleatoire.Next(0, (int)JeuCanva.ActualWidth - 21));

                JeuCanva.Children.Add(powerUp);
                listePowerUps.Add(powerUp);
            }
        }

        private void DeplacerPowerUp(Rectangle powerUp)
        {
            double top = Canvas.GetTop(powerUp);
            Canvas.SetTop(powerUp, top + vitesseShuriken / 2);

            if (top > JeuCanva.ActualHeight)
            {
                JeuCanva.Children.Remove(powerUp);
                listePowerUps.Remove(powerUp);
            }
        }

        private void CreerShurikens()
        {
            AjouterShurikenACanva("shuriken1.png", 45, 37.5);
            AjouterShurikenACanva("shuriken2.png", 37.5, 60);
            AjouterShurikenACanva("shuriken1.png", 45, 37.5);
        }

        private void AjouterShurikenACanva(string imageShuriken, double largeur, double hauteur)
        {
            Rectangle shuriken = new Rectangle
            {
                Width = largeur,
                Height = hauteur,
                Fill = new ImageBrush(new BitmapImage(new Uri($"pack://application:,,,/{assemblyName};component/{imageShuriken}", UriKind.Absolute)))
            };

            Canvas.SetTop(shuriken, -hauteur);
            int maxLargeur = Math.Max(0, (int)JeuCanva.ActualWidth - (int)largeur);
            Canvas.SetLeft(shuriken, aleatoire.Next(0, maxLargeur));

            JeuCanva.Children.Add(shuriken);
            listeShuriken.Add(shuriken);
        }

        private void DeplacerShuriken(Rectangle shuriken)
        {
            double top = Canvas.GetTop(shuriken);
            Canvas.SetTop(shuriken, top + vitesseShuriken);

            if (top > JeuCanva.ActualHeight)
            {
                ReinitialiserPositionShuriken(shuriken);
                score++;
            }
        }

        private void ReinitialiserPositionShuriken(Rectangle shuriken)
        {
            Canvas.SetTop(shuriken, -shuriken.Height);
            Canvas.SetLeft(shuriken, aleatoire.Next(0, (int)JeuCanva.ActualWidth));
        }

        private void NettoyerObjetsInutilises()
        {
            for (int i = listePowerUps.Count - 1; i >= 0; i--)
            {
                Rectangle powerUp = listePowerUps[i];
                if (Canvas.GetTop(powerUp) > JeuCanva.ActualHeight && JeuCanva.Children.Contains(powerUp))
                {
                    JeuCanva.Children.Remove(powerUp);
                    listePowerUps.RemoveAt(i);
                }
            }
        }

        private bool CollisionAvecNinja(Rectangle objet)
        {
            ScaleTransform scaleTransform = PersoRect.RenderTransform as ScaleTransform;
            double scaleX = scaleTransform?.ScaleX ?? 1.0;
            double scaleY = scaleTransform?.ScaleY ?? 1.0;

            double ninjaLeft = Canvas.GetLeft(PersoRect);
            double ninjaTop = Canvas.GetTop(PersoRect);
            double ninjaWidth = PersoRect.Width;
            double ninjaHeight = PersoRect.Height;

            double hitboxPercentWidth = 0.3; // Utilise 30% de la largeur
            double hitboxPercentHeight = 0.4; // Utilise 40% de la hauteur

            double hitboxWidth = ninjaWidth * scaleX * hitboxPercentWidth;
            double hitboxHeight = ninjaHeight * scaleY * hitboxPercentHeight;

            double hitboxLeft = ninjaLeft + (ninjaWidth * scaleX - hitboxWidth) / 2;
            double hitboxTop = ninjaTop + (ninjaHeight * scaleY * 0.4);

            Rect ninjaPos = new Rect(hitboxLeft, hitboxTop, hitboxWidth, hitboxHeight);
            Rect objetPos = new Rect(Canvas.GetLeft(objet), Canvas.GetTop(objet), objet.Width, objet.Height);

            return ninjaPos.IntersectsWith(objetPos);
        }

        private void AnimerCollision(Rectangle shuriken)
        {
            DoubleAnimation animation = new DoubleAnimation
            {
                From = 1.0,
                To = 0.0,
                Duration = new Duration(TimeSpan.FromSeconds(0.5)),
                AutoReverse = true
            };
            shuriken.BeginAnimation(UIElement.OpacityProperty, animation);
        }

        private void MouvementNinja()
        {
            double nouvellePositionX = Canvas.GetLeft(PersoRect);

            if (droite)
            {
                nouvellePositionX += 12;
                if (nouvellePositionX + PersoRect.ActualWidth > JeuCanva.ActualWidth)
                {
                    nouvellePositionX = JeuCanva.ActualWidth - PersoRect.ActualWidth;
                }
            }
            else if (gauche)
            {
                nouvellePositionX -= 12;
                if (nouvellePositionX < 0)
                {
                    nouvellePositionX = 0;
                }
            }

            Canvas.SetLeft(PersoRect, nouvellePositionX);

            if (!isHurt)
            {
                if (droite)
                {
                    idleAnimation.Stop();
                    runAnimation.Start();
                }
                else if (gauche)
                {
                    idleAnimation.Stop();
                    runLeftAnimation.Start();
                }
                else
                {
                    runAnimation.Stop();
                    runLeftAnimation.Stop();
                    idleAnimation.Start();
                }
            }
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.Key)
            {
                case Key.Right:
                    droite = true;
                    break;
                case Key.Left:
                    gauche = true;
                    break;
                case Key.Add:
                    ActiverInvincible();
                    break;
                case Key.Subtract:
                    DesactiverInvincible();
                    break;
                case Key.Escape:
                    Application.Current.Shutdown();
                    break;
                case Key.Space:
                    if (!isHurt)
                    {
                        attackAnimation.Start();
                        DispatcherTimer attackTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(0.3) };
                        attackTimer.Tick += (s, e) =>
                        {
                            attackAnimation.Stop();
                            attackTimer.Stop();
                        };
                        attackTimer.Start();
                    }
                    break;
                case Key.P:
                    GererPause();
                    break;
            }
        }

        private void Window_KeyUp(object sender, KeyEventArgs e)
        {
            switch (e.Key)
            {
                case Key.Right:
                    droite = false;
                    break;
                case Key.Left:
                    gauche = false;
                    break;
            }
        }

        public bool ActiverInvincible()
        {
            modeInvincible = true;

            InvincibleText.Visibility = Visibility.Visible;

            DoubleAnimation pulseAnimation = new DoubleAnimation
            {
                From = 1.0,
                To = 1.2,
                Duration = new Duration(TimeSpan.FromSeconds(0.5)),
                AutoReverse = true,
                RepeatBehavior = RepeatBehavior.Forever
            };

            InvincibleTextScale.BeginAnimation(ScaleTransform.ScaleXProperty, pulseAnimation);
            InvincibleTextScale.BeginAnimation(ScaleTransform.ScaleYProperty, pulseAnimation);

            DoubleAnimation opacityAnimation = new DoubleAnimation
            {
                From = 1.0,
                To = 0.6,
                Duration = new Duration(TimeSpan.FromSeconds(0.3)),
                AutoReverse = true,
                RepeatBehavior = RepeatBehavior.Forever
            };

            PersoRect.BeginAnimation(UIElement.OpacityProperty, opacityAnimation);

            DispatcherTimer timerInvincible = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(5)
            };
            timerInvincible.Tick += (s, e) => {
                DesactiverInvincible();
                timerInvincible.Stop();
            };
            timerInvincible.Start();

            return modeInvincible;
        }

        public bool DesactiverInvincible()
        {
            modeInvincible = false;

            InvincibleText.Visibility = Visibility.Collapsed;

            InvincibleTextScale.BeginAnimation(ScaleTransform.ScaleXProperty, null);
            InvincibleTextScale.BeginAnimation(ScaleTransform.ScaleYProperty, null);
            PersoRect.BeginAnimation(UIElement.OpacityProperty, null);

            return modeInvincible;
        }

        private int SauvegarderHighScore(int score)
        {
            try
            {
                string cheminFichier = "highscores.txt";
                int highscore = 0;

                if (File.Exists(cheminFichier))
                {
                    string highscoreTexte = File.ReadAllText(cheminFichier);
                    int.TryParse(highscoreTexte, out highscore);
                }

                if (score > highscore)
                {
                    File.WriteAllText(cheminFichier, score.ToString());
                    return score;
                }

                return highscore;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la sauvegarde du score: {ex.Message}", "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
                return 0;
            }
        }

        private void GererPause()
        {
            pause = !pause;

            PauseBar1.Visibility = pause ? Visibility.Visible : Visibility.Collapsed;
            PauseBar2.Visibility = pause ? Visibility.Visible : Visibility.Collapsed;

            if (pause)
            {
                minuterie.Stop();
            }
            else
            {
                minuterie.Start();
            }
        }

        public void AfficherScoreEtVie(int score, int vieRestant)
        {
            ScoreText.Text = $"Score: {score}";
            VieRestant.Text = $"Vie Restantes: {vieRestant}";
        }

        public void FinDuJeu()
        {
            minuterie.Stop();
            int highscore = SauvegarderHighScore(score);

            ResultatScore resultatScore = new ResultatScore();
            resultatScore.AfficherScoreFinal(score, highscore);
            resultatScore.ShowDialog();
        }
    }

    public class SpriteAnimation : IDisposable
    {
        private readonly ImageBrush _targetBrush;
        private readonly BitmapImage _spriteSheet;
        private readonly int _frameCount;
        private readonly int _frameWidth;
        private readonly int _frameHeight;
        private readonly DispatcherTimer _timer;
        private int _currentFrame;

        public bool IsRunning => _timer.IsEnabled;

        public SpriteAnimation(ImageBrush target, string spriteSheetPath,
                             int frameWidth, int frameHeight, int frameCount, double fps)
        {
            _targetBrush = target;
            _frameWidth = frameWidth;
            _frameHeight = frameHeight;
            _frameCount = frameCount;

            _spriteSheet = new BitmapImage(new Uri(spriteSheetPath, UriKind.RelativeOrAbsolute));

            _timer = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(1 / fps)
            };
            _timer.Tick += UpdateFrame;
        }

        private void UpdateFrame(object sender, EventArgs e)
        {
            _currentFrame = (_currentFrame + 1) % _frameCount;

            var cropped = new CroppedBitmap(_spriteSheet,
                new Int32Rect(_currentFrame * _frameWidth, 0, _frameWidth, _frameHeight));

            _targetBrush.ImageSource = cropped;
        }

        public void Start() => _timer.Start();
        public void Stop() => _timer.Stop();

        public void Dispose()
        {
            _timer.Stop();
            _timer.Tick -= UpdateFrame;
        }
    }
}
