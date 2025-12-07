import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';

interface RoleDefinitionModalProps {
  open: boolean;
  roomId: string;
  onSuccess: () => void;
}

export function RoleDefinitionModal({
  open,
  roomId,
  onSuccess,
}: RoleDefinitionModalProps) {
  const [role, setRole] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!role.trim()) return;

    setError(null);
    setLoading(true);

    try {
      await api.put(`/api/rooms/${roomId}/role`, {
        role: role.trim(),
      });
      setRole('');
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de la définition du rôle');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={() => {}}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Définir votre identité</DialogTitle>
          <DialogDescription>
            Décrivez qui vous êtes pour que l'IA puisse identifier qui pose les questions. Cela peut être n'importe quoi : votre rôle professionnel, votre fonction, ou simplement une description de vous-même.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
                {error}
              </div>
            )}
            <div className="space-y-2">
              <label htmlFor="role" className="text-sm font-medium">
                Qui êtes-vous ?
              </label>
              <Input
                id="role"
                placeholder="Ex: Développeur Backend, Designer UX, Étudiant en informatique, Chef de projet..."
                value={role}
                onChange={(e) => setRole(e.target.value)}
                disabled={loading}
                autoFocus
              />
              <p className="text-xs text-muted-foreground">
                Décrivez-vous en quelques mots. L'IA utilisera cette information pour savoir qui pose les questions.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" disabled={!role.trim() || loading}>
              {loading ? 'Enregistrement...' : 'Confirmer'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

