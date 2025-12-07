import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Check, Plus, X, Trash2 } from 'lucide-react';
import { Socket } from 'socket.io-client';

interface MessageValidation {
  id: string;
  member_id: string;
  action: 'validated' | 'added' | 'rejected';
  addition?: string;
  comment?: string;
  username?: string;
  role?: string;
}

interface PendingMessageCardProps {
  message: {
    id: string;
    user_id: string;
    username?: string;
    role?: string;
    content: string;
    created_at: string;
    status: string;
  };
  currentUserId: string;
  members: Array<{ id: string; username: string; role: string | null }>;
  validations: MessageValidation[];
  validationsCount: number;
  totalMembers: number;
  socket: Socket | null;
  onRetract?: () => void;
}

export function PendingMessageCard({
  message,
  currentUserId,
  members: _members,
  validations,
  validationsCount,
  totalMembers,
  socket,
  onRetract,
}: PendingMessageCardProps) {
  const [showAddModal, setShowAddModal] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [addition, setAddition] = useState('');
  const [rejectComment, setRejectComment] = useState('');

  const isAuthor = message.user_id && currentUserId && message.user_id === currentUserId;
  const hasValidated = validations.some((v) => v.member_id === currentUserId);
  const canRetract = isAuthor && validations.length === 0;

  const handleValidate = () => {
    if (!socket) return;
    socket.emit('validate-message', {
      messageId: message.id,
      action: 'validated',
    });
  };

  const handleAdd = () => {
    if (!socket || !addition.trim()) return;
    socket.emit('validate-message', {
      messageId: message.id,
      action: 'added',
      addition: addition.trim(),
    });
    setShowAddModal(false);
    setAddition('');
  };

  const handleReject = () => {
    if (!socket) return;
    socket.emit('validate-message', {
      messageId: message.id,
      action: 'rejected',
      comment: rejectComment.trim() || undefined,
    });
    setShowRejectModal(false);
    setRejectComment('');
  };

  const handleRetract = () => {
    if (!socket || !canRetract) return;
    socket.emit('retract-message', { messageId: message.id });
    if (onRetract) onRetract();
  };

  return (
    <>
      <Card className="border-yellow-300 bg-yellow-50/50 p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-semibold text-sm">
                {message.username}
                {message.role && (
                  <span className="text-muted-foreground font-normal">
                    {' '}({message.role})
                  </span>
                )}
              </span>
              <Badge variant="warning">En attente de validation</Badge>
            </div>
            <p className="text-sm whitespace-pre-wrap mt-2">{message.content}</p>
          </div>
        </div>

        {/* Indicateur de progression */}
        <div className="mt-3 text-xs text-muted-foreground">
          {validationsCount} / {totalMembers} membre(s) ont validé
        </div>

        {/* Liste des validations */}
        {validations.length > 0 && (
          <div className="mt-3 space-y-1">
            {validations.map((validation) => (
              <div key={validation.id} className="text-xs flex items-center gap-2">
                <span className="font-medium">{validation.username}</span>
                {validation.action === 'validated' && (
                  <Badge variant="success" className="text-xs py-0">
                    <Check className="h-3 w-3 mr-1" />
                    Validé
                  </Badge>
                )}
                {validation.action === 'added' && (
                  <Badge variant="secondary" className="text-xs py-0">
                    <Plus className="h-3 w-3 mr-1" />
                    Ajouté: {validation.addition}
                  </Badge>
                )}
                {validation.action === 'rejected' && (
                  <Badge variant="destructive" className="text-xs py-0">
                    <X className="h-3 w-3 mr-1" />
                    Rejeté
                  </Badge>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Actions */}
        <div className="mt-4 flex gap-2 flex-wrap">
          {isAuthor ? (
            canRetract && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleRetract}
                className="text-xs"
              >
                <Trash2 className="h-3 w-3 mr-1" />
                Retirer
              </Button>
            )
          ) : (
            !hasValidated && (
              <>
                <Button
                  variant="default"
                  size="sm"
                  onClick={handleValidate}
                  className="text-xs"
                >
                  <Check className="h-3 w-3 mr-1" />
                  Valider
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => setShowAddModal(true)}
                  className="text-xs"
                >
                  <Plus className="h-3 w-3 mr-1" />
                  Ajouter
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => setShowRejectModal(true)}
                  className="text-xs"
                >
                  <X className="h-3 w-3 mr-1" />
                  Rejeter
                </Button>
              </>
            )
          )}
        </div>
      </Card>

      {/* Modal Ajouter */}
      <Dialog open={showAddModal} onOpenChange={setShowAddModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Ajouter quelque chose</DialogTitle>
            <DialogDescription>
              Ajoutez du contenu au message de {message.username}
            </DialogDescription>
          </DialogHeader>
          <Textarea
            placeholder="Votre ajout..."
            value={addition}
            onChange={(e) => setAddition(e.target.value)}
            className="min-h-[100px]"
          />
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddModal(false)}>
              Annuler
            </Button>
            <Button onClick={handleAdd} disabled={!addition.trim()}>
              Ajouter
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Modal Rejeter */}
      <Dialog open={showRejectModal} onOpenChange={setShowRejectModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Rejeter le message</DialogTitle>
            <DialogDescription>
              Expliquez pourquoi vous rejetez ce message (optionnel)
            </DialogDescription>
          </DialogHeader>
          <Textarea
            placeholder="Commentaire de rejet (optionnel)..."
            value={rejectComment}
            onChange={(e) => setRejectComment(e.target.value)}
            className="min-h-[100px]"
          />
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowRejectModal(false)}>
              Annuler
            </Button>
            <Button variant="destructive" onClick={handleReject}>
              Rejeter
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}

