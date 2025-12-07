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
import { useToast } from '@/hooks/use-toast';

interface InviteModalProps {
  open: boolean;
  roomId: string;
  currentMembers: number;
  onClose: () => void;
  onSuccess?: () => void;
}

export function InviteModal({
  open,
  roomId,
  currentMembers,
  onClose,
  onSuccess,
}: InviteModalProps) {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) return;

    if (currentMembers >= 4) {
      setError('La room a déjà atteint le maximum de 4 membres');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      await api.post('/api/invitations', {
        roomId,
        recipientUsername: username.trim(),
      });
      toast({
        title: 'Invitation envoyée',
        description: `Une invitation a été envoyée à ${username.trim()}`,
        variant: 'success',
      });
      setUsername('');
      onClose();
      if (onSuccess) onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de l\'envoi de l\'invitation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Inviter un membre</DialogTitle>
          <DialogDescription>
            Invitez un utilisateur à rejoindre cette conversation. Maximum 4 membres par conversation.
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
              <label htmlFor="username" className="text-sm font-medium">
                Nom d'utilisateur
              </label>
              <Input
                id="username"
                placeholder="nom_utilisateur"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
                autoFocus
              />
              <p className="text-xs text-muted-foreground">
                {currentMembers} / 4 membre(s) dans cette conversation
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose} disabled={loading}>
              Annuler
            </Button>
            <Button type="submit" disabled={!username.trim() || loading || currentMembers >= 4}>
              {loading ? 'Envoi...' : 'Envoyer l\'invitation'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

