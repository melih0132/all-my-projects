using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Windows.Threading;

namespace NinjaJeu
{
    public partial class MainWindow : Window
    {
        private int score = 0;
        private int vie = 3;
        private int vieRestant;
        private bool vieAjoutee = false;
        private int vitesseShuriken = 10;

        private bool augmentationFaite = false;
        private bool modeInvincible = false;
        private bool pause = false;
        private bool gauche = false;
        private bool droite = false;

        public static MediaPlayer musqiueDeFond = new MediaPlayer();
        DispatcherTimer minuterie = new DispatcherTimer();
        List<Rectangle> listeShuriken = new List<Rectangle>();
        Random aleatoire = new Random();

        //test github modif

        public MainWindow()
        {
            InitializeComponent();

            musqiueDeFond.Open(new Uri("SonFond.mp3", UriKind.Relative));
            musqiueDeFond.Volume = 0.1;
            musqiueDeFond.Play();

            EntreeEnJeu entreeEnJeu = new EntreeEnJeu();
            entreeEnJeu.ShowDialog();

            if (entreeEnJeu.DialogResult == true)
            {
                CreerShurikens();
            }

            InitialiserJeu();
        }

        public static void GererMusqiueDeFond()
        {
            musqiueDeFond.IsMuted = !musqiueDeFond.IsMuted;
        }

        public static bool RenvoieTrueSiMusqiueDeFondDesactive()
        {
            return musqiueDeFond.IsMuted;
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
            if (!minuterie.IsEnabled)
            {
                minuterie.Start();
            }

            minuterie.Tick += BoucleJeu;

            KeyDown -= Window_KeyDown;
            KeyDown += Window_KeyDown;
            KeyUp -= Window_KeyUp;
            KeyUp += Window_KeyUp;

            CreerShurikens();

            AfficherScoreEtVie(score, vieRestant);
        }

        private void BoucleJeu(object? sender, EventArgs e)
        {
            if (pause)
            {
                return;
            }

            GestionModifVitesseShuriken();

            AjouterVie();

            foreach (Rectangle shuriken in listeShuriken)
            {
                DeplacerShuriken(shuriken);
                AfficherScoreEtVie(score, vieRestant);
                if (CollisionAvecNinja(shuriken))
                {
                    if (!modeInvincible)
                    {
                        vieRestant--;

                        Canvas.SetTop(shuriken, -shuriken.Height);
                        Canvas.SetLeft(shuriken, aleatoire.Next(0, (int)JeuCanva.ActualWidth));
                    }

                    if (vieRestant <= 0)
                    {
                        FinDuJeu();
                        return;
                    }
                }
            }

            MouvementNinja();
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
            if (score % 10 == 0 && !augmentationFaite)
            {
                vitesseShuriken += 2; 
                augmentationFaite = true;
            }
            else if (score % 10 != 0)
            {
                augmentationFaite = false; 
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
                Fill = new ImageBrush(new BitmapImage(new Uri($"pack://application:,,,/{imageShuriken}", UriKind.Absolute)))
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
                Canvas.SetTop(shuriken, -shuriken.Height);
                Canvas.SetLeft(shuriken, aleatoire.Next(0, (int)JeuCanva.ActualWidth));

                score++;
            }
        }

        private bool CollisionAvecNinja(Rectangle shuriken)
        {
            Rect ninjaPos = new Rect(Canvas.GetLeft(PersoRect), Canvas.GetTop(PersoRect), PersoRect.Width, PersoRect.Height);
            Rect shurikenPos = new Rect(Canvas.GetLeft(shuriken), Canvas.GetTop(shuriken), shuriken.Width, shuriken.Height);

            bool collision = ninjaPos.IntersectsWith(shurikenPos);
            return collision;
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
            return modeInvincible;
        }

        public bool DesactiverInvincible()
        {
            modeInvincible = false;
            return modeInvincible;
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
            ResultatScore resultatScore = new ResultatScore();
            resultatScore.AfficherScoreFinal(score); 
            resultatScore.ShowDialog();
        }
    }
}