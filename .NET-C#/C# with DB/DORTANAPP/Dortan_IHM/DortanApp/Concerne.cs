using System;

namespace DortanApp
{
    public class Concerne
    {
        private Reservation reservation;
        private Materiel material;

        public Concerne(Reservation reservation, Materiel material)
        {
            this.Reservation = reservation;
            this.Material = material;
        }

        public Reservation Reservation
        {
            get
            {
                return reservation;
            }

            set
            {
                reservation = value;
            }
        }

        public Materiel Material
        {
            get
            {
                return this.material;
            }

            set
            {
                this.material = value;
            }
        }
    }
}