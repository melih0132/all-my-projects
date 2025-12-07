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
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Socket } from 'socket.io-client';

interface ConflictMessage {
  id: string;
  user_id: string | null;
  username?: string;
  role?: string;
  content: string;
  created_at: string;
}

interface ConflictVoteModalProps {
  open: boolean;
  conflictId: string;
  messages: ConflictMessage[];
  votesCount: number;
  totalMembers: number;
  socket: Socket | null;
  onClose: () => void;
}

export function ConflictVoteModal({
  open,
  conflictId,
  messages,
  votesCount,
  totalMembers,
  socket,
  onClose,
}: ConflictVoteModalProps) {
  const [selectedMessageId, setSelectedMessageId] = useState<string | null>(null);

  const handleVote = () => {
    if (!socket || !selectedMessageId) return;
    socket.emit('vote-message', {
      conflictId,
      messageId: selectedMessageId,
    });
    onClose();
    setSelectedMessageId(null);
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Conflit de Messages</DialogTitle>
          <DialogDescription>
            Plusieurs membres ont envoyé des messages simultanément. Votez pour celui qui doit être traité en premier.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-3 max-h-[400px] overflow-y-auto">
          {messages.map((message) => (
            <Card
              key={message.id}
              className={`p-4 cursor-pointer transition-all ${
                selectedMessageId === message.id
                  ? 'border-primary bg-primary/5'
                  : 'hover:bg-accent'
              }`}
              onClick={() => setSelectedMessageId(message.id)}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-sm">
                    {message.username}
                    {message.role && (
                      <span className="text-muted-foreground font-normal">
                        {' '}({message.role})
                      </span>
                    )}
                  </span>
                </div>
                {selectedMessageId === message.id && (
                  <Badge variant="default">Sélectionné</Badge>
                )}
              </div>
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </Card>
          ))}
        </div>

        <div className="text-sm text-muted-foreground">
          {votesCount} / {totalMembers} vote(s) reçu(s)
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Annuler
          </Button>
          <Button
            onClick={handleVote}
            disabled={!selectedMessageId}
          >
            Voter pour ce message
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

