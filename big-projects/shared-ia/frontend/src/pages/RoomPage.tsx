import { useEffect, useState, useRef, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { getSocket } from '@/lib/socket';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Skeleton } from '@/components/ui/skeleton';
import { PendingMessageCard } from '@/components/PendingMessageCard';
import { ConflictVoteModal } from '@/components/ConflictVoteModal';
import { InviteModal } from '@/components/InviteModal';
import { RoleDefinitionModal } from '@/components/RoleDefinitionModal';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ArrowLeft, MoreVertical, Edit, Trash2, UserPlus, Loader2 } from 'lucide-react';
import { Socket } from 'socket.io-client';
import { useToast } from '@/hooks/use-toast';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  room_id: string;
  user_id: string | null;
  type: 'user' | 'ai' | 'system';
  status: string;
  content: string;
  created_at: string;
  edited_at?: string;
  username?: string;
  role?: string;
  validations?: MessageValidation[];
}

interface MessageValidation {
  id: string;
  member_id: string;
  action: 'validated' | 'added' | 'rejected';
  addition?: string;
  comment?: string;
  username?: string;
  role?: string;
}

interface Member {
  id: string;
  username: string;
  role: string | null;
  isOnline?: boolean;
  isTyping?: boolean;
}

interface Conflict {
  id: string;
  messages: Array<Omit<Message, 'user_id'> & { user_id: string }>;
  votesCount: number;
  totalMembers: number;
}

export default function RoomPage() {
  const { roomId } = useParams<{ roomId: string }>();
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const { toast } = useToast();
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [members, setMembers] = useState<Member[]>([]);
  const [room, setRoom] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [messageInput, setMessageInput] = useState('');
  const [typingMembers, setTypingMembers] = useState<Set<string>>(new Set());
  const [pendingMessage, setPendingMessage] = useState<Message | null>(null);
  const [conflict, setConflict] = useState<Conflict | null>(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingMessage, setEditingMessage] = useState<Message | null>(null);
  const [editContent, setEditContent] = useState('');
  const [inviteModalOpen, setInviteModalOpen] = useState(false);
  const [roleModalOpen, setRoleModalOpen] = useState(false);
  const [deleteRoomDialogOpen, setDeleteRoomDialogOpen] = useState(false);
  const [isDeletingRoom, setIsDeletingRoom] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Fonction pour trier les messages par created_at
  const sortMessages = useCallback((msgs: Message[]): Message[] => {
    return [...msgs].sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
  }, []);

  // Scroll vers le bas
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Gestion de la connexion Socket.io avec reconnexion
  useEffect(() => {
    if (!roomId) return;

    const socketInstance = getSocket();
    setSocket(socketInstance);

    // Gestion de la reconnexion
    socketInstance.on('connect', () => {
      console.log('Socket.io connecté');
      socketInstance.emit('join-room', roomId);
      toast({
        title: 'Connexion rétablie',
        description: 'Vous êtes de nouveau connecté',
        variant: 'success',
      });
    });

    socketInstance.on('disconnect', () => {
      console.log('Socket.io déconnecté');
      toast({
        title: 'Connexion perdue',
        description: 'Tentative de reconnexion...',
        variant: 'default',
      });
    });

    socketInstance.on('reconnect', () => {
      console.log('Socket.io reconnecté');
      socketInstance.emit('join-room', roomId);
    });

    // Rejoindre la room
    socketInstance.emit('join-room', roomId);

    // Écouter les événements
    socketInstance.on('room-joined', (data: any) => {
      setRoom(data.room);
      setMembers(data.members || []);
      setMessages(sortMessages(data.messages || []));
      setLoading(false);
      
      // Vérifier si l'utilisateur doit définir son rôle
      const currentMember = data.members?.find((m: Member) => m.id === user?.id);
      if (currentMember && !currentMember.role) {
        setRoleModalOpen(true);
      }
    });

    socketInstance.on('new-pending-message', (message: Message) => {
      setPendingMessage(message);
      setMessages((prev) => {
        // Vérifier si le message existe déjà
        if (prev.some((m) => m.id === message.id)) {
          return prev;
        }
        return [...prev, message];
      });
      toast({
        title: 'Nouveau message en attente',
        description: `${message.username} a envoyé un message`,
      });
    });

    socketInstance.on('validation-update', (data: {
      messageId: string;
      validation: MessageValidation;
      validationsCount: number;
      totalMembers: number;
    }) => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === data.messageId
            ? {
                ...msg,
                validations: [
                  ...(msg.validations || []),
                  data.validation,
                ],
              }
            : msg
        )
      );
      setPendingMessage((prev) =>
        prev?.id === data.messageId
          ? {
              ...prev,
              validations: [
                ...(prev.validations || []),
                data.validation,
              ],
            }
          : prev
      );
    });

    socketInstance.on('message-rejected', (data: {
      messageId: string;
      validation: MessageValidation;
    }) => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === data.messageId
            ? { ...msg, status: 'rejected', validations: [...(msg.validations || []), data.validation] }
            : msg
        )
      );
      setPendingMessage(null);
      toast({
        title: 'Message rejeté',
        description: data.validation.comment || 'Le message a été rejeté',
        variant: 'destructive',
      });
    });

    socketInstance.on('message-retracted', (data: { messageId: string }) => {
      setMessages((prev) => prev.filter((msg) => msg.id !== data.messageId));
      setPendingMessage(null);
    });

    socketInstance.on('message-validated', (data: { message: Message }) => {
      // Ajouter ou mettre à jour le message validé dans la liste
      setMessages((prev) => {
        const existingIndex = prev.findIndex((msg) => msg.id === data.message.id);
        let updated;
        
        if (existingIndex >= 0) {
          // Le message existe déjà, le mettre à jour
          updated = prev.map((msg) =>
            msg.id === data.message.id
              ? { ...data.message, status: 'validated' }
              : msg
          );
        } else {
          // Le message n'existe pas encore (cas de validation automatique), l'ajouter
          updated = [...prev, { ...data.message, status: 'validated' }];
        }
        
        return sortMessages(updated);
      });
      // Retirer le message en attente
      setPendingMessage(null);
      // Nettoyer l'indicateur de frappe pour l'auteur du message
      if (data.message.user_id) {
        setTypingMembers((prev) => {
          const next = new Set(prev);
          next.delete(data.message.user_id!);
          return next;
        });
      }
    });

    socketInstance.on('ai-response-start', (data: { messageId: string }) => {
      // Insérer le message streaming après le message validé
      // Les messages sont triés par created_at, donc le message validé (créé avant) sera avant le streaming
      setMessages((prev) => {
        // Retirer le message en attente s'il existe encore
        const filtered = prev.filter((msg) => !(msg.id === data.messageId && msg.status === 'pending_validation'));
        
        // Trouver l'auteur du message validé pour nettoyer son indicateur de frappe
        const validatedMessage = prev.find((msg) => msg.id === data.messageId);
        if (validatedMessage?.user_id) {
          setTypingMembers((prevTyping) => {
            const next = new Set(prevTyping);
            next.delete(validatedMessage.user_id!);
            return next;
          });
        }
        
        // Ajouter le message streaming (il sera trié par created_at)
        const streamingMessage: Message = {
          id: 'streaming',
          room_id: roomId!,
          user_id: null,
          type: 'ai',
          status: 'sent',
          content: '',
          created_at: new Date().toISOString(),
        };
        
        return sortMessages([...filtered, streamingMessage]);
      });
      
      // Nettoyer tous les indicateurs de frappe quand l'IA commence à répondre
      setTypingMembers(new Set());
    });

    socketInstance.on('ai-response-chunk', (data: { messageId: string; content: string }) => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === 'streaming'
            ? { ...msg, content: msg.content + data.content }
            : msg
        )
      );
    });

    socketInstance.on('ai-response-end', (data: { messageId: string; aiMessage: Message }) => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === 'streaming' ? data.aiMessage : msg
        )
      );
    });

    socketInstance.on('ai-response-error', (data: {
      messageId: string;
      error: string;
      canRetry: boolean;
    }) => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === data.messageId
            ? { ...msg, status: 'error', content: `Erreur: ${data.error}` }
            : msg
        )
      );
      toast({
        title: 'Erreur IA',
        description: data.error,
        variant: 'destructive',
      });
    });

    socketInstance.on('conflict-detected', (data: {
      conflictId: string;
      messages: Message[];
    }) => {
      const totalMembers = members.length;
      setConflict({
        id: data.conflictId,
        messages: data.messages.map(msg => ({
          ...msg,
          user_id: msg.user_id || '',
        })),
        votesCount: 0,
        totalMembers,
      });
      toast({
        title: 'Conflit détecté',
        description: 'Plusieurs messages ont été envoyés simultanément',
      });
    });

    socketInstance.on('vote-update', (data: {
      conflictId: string;
      votesCount: number;
      totalMembers: number;
    }) => {
      setConflict((prev) =>
        prev?.id === data.conflictId
          ? { ...prev, votesCount: data.votesCount, totalMembers: data.totalMembers }
          : prev
      );
    });

    socketInstance.on('conflict-resolved', (data: {
      winnerId: string;
      message: Message;
    }) => {
      setConflict(null);
      setPendingMessage(data.message);
      setMessages((prev) => [...prev, data.message]);
      toast({
        title: 'Conflit résolu',
        description: 'Un message a été sélectionné',
        variant: 'success',
      });
    });

    socketInstance.on('message-edited', (data: {
      message: Message;
      deletedAfter: string;
    }) => {
      setMessages((prev) => {
        const index = prev.findIndex((m) => m.id === data.message.id);
        if (index === -1) return prev;
        const before = prev.slice(0, index + 1);
        return [
          ...before,
          { ...data.message, status: 'pending_validation' },
        ];
      });
      toast({
        title: 'Message édité',
        description: 'Le message et les suivants ont été supprimés',
      });
    });

    socketInstance.on('messages-deleted', (data: { deletedFrom: string }) => {
      setMessages((prev) => {
        const index = prev.findIndex((m) => m.created_at >= data.deletedFrom);
        return index === -1 ? prev : prev.slice(0, index);
      });
    });

    socketInstance.on('member-joined', (data: { member: Member; systemMessage: Message }) => {
      setMembers((prev) => {
        if (prev.some((m) => m.id === data.member.id)) return prev;
        return [...prev, data.member];
      });
      setMessages((prev) => [...prev, data.systemMessage]);
    });

    socketInstance.on('member-left', (data: { memberId: string; systemMessage: Message }) => {
      setMembers((prev) => prev.filter((m) => m.id !== data.memberId));
      setMessages((prev) => [...prev, data.systemMessage]);
    });

    socketInstance.on('typing-update', (data: {
      userId: string;
      username: string;
      isTyping: boolean;
    }) => {
      if (data.userId === user?.id) return;
      setTypingMembers((prev) => {
        const next = new Set(prev);
        if (data.isTyping) {
          next.add(data.userId);
        } else {
          next.delete(data.userId);
        }
        return next;
      });
    });

    socketInstance.on('error', (error: { message: string }) => {
      console.error('Erreur Socket.io:', error);
      
      // Rediriger vers le dashboard si l'erreur indique que la room n'existe pas ou que l'utilisateur n'est plus membre
      if (
        error.message.includes('n\'etes pas membre') ||
        error.message.includes('Room introuvable') ||
        error.message.includes('n\'existe pas')
      ) {
        toast({
          title: 'Room inaccessible',
          description: error.message,
          variant: 'destructive',
        });
        navigate('/dashboard');
        return;
      }
      
      toast({
        title: 'Erreur',
        description: error.message,
        variant: 'destructive',
      });
    });

    socketInstance.on('room-not-found', () => {
      toast({
        title: 'Room introuvable',
        description: 'Cette conversation n\'existe plus ou a été supprimée',
        variant: 'destructive',
      });
      navigate('/dashboard');
    });

    socketInstance.on('room-deleted', () => {
      toast({
        title: 'Conversation supprimée',
        description: 'Cette conversation a été supprimée',
        variant: 'destructive',
      });
      navigate('/dashboard');
    });

    return () => {
      socketInstance.emit('leave-room', roomId);
      socketInstance.off('connect');
      socketInstance.off('disconnect');
      socketInstance.off('reconnect');
      socketInstance.off('room-joined');
      socketInstance.off('new-pending-message');
      socketInstance.off('validation-update');
      socketInstance.off('message-rejected');
      socketInstance.off('message-retracted');
      socketInstance.off('message-validated');
      socketInstance.off('ai-response-start');
      socketInstance.off('ai-response-chunk');
      socketInstance.off('ai-response-end');
      socketInstance.off('ai-response-error');
      socketInstance.off('conflict-detected');
      socketInstance.off('vote-update');
      socketInstance.off('conflict-resolved');
      socketInstance.off('message-edited');
      socketInstance.off('messages-deleted');
      socketInstance.off('member-joined');
      socketInstance.off('member-left');
      socketInstance.off('typing-update');
      socketInstance.off('error');
      socketInstance.off('room-not-found');
      socketInstance.off('room-deleted');
    };
  }, [roomId, user?.id, toast]);

  const handleSendMessage = () => {
    if (!messageInput.trim() || !socket || !roomId) return;

    socket.emit('send-message', {
      roomId,
      content: messageInput.trim(),
    });

    setMessageInput('');
    // Arrêter l'indicateur de frappe
    socket.emit('typing', { roomId, isTyping: false });
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
  };

  const handleTyping = (typing: boolean) => {
    if (!socket || !roomId) return;
    socket.emit('typing', { roomId, isTyping: typing });

    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    if (typing) {
      typingTimeoutRef.current = setTimeout(() => {
        socket.emit('typing', { roomId, isTyping: false });
      }, 3000);
    }
  };

  const handleEditMessage = (message: Message) => {
    setEditingMessage(message);
    setEditContent(message.content);
    setEditDialogOpen(true);
  };

  const handleConfirmEdit = () => {
    if (!socket || !editingMessage || !editContent.trim()) return;

    socket.emit('edit-message', {
      messageId: editingMessage.id,
      newContent: editContent.trim(),
    });

    setEditDialogOpen(false);
    setEditingMessage(null);
    setEditContent('');
  };

  const handleDeleteMessage = (messageId: string) => {
    if (!socket || !confirm('Êtes-vous sûr de vouloir supprimer ce message ? Tous les messages suivants seront également supprimés.')) return;

    socket.emit('delete-message', { messageId });
  };

  const handleRetryAI = (messageId: string) => {
    if (!socket || !roomId) return;
    socket.emit('retry-ai-message', { messageId, roomId });
  };

  const handleDeleteRoom = async () => {
    if (!roomId) return;
    
    setIsDeletingRoom(true);
    try {
      await api.delete(`/api/rooms/${roomId}`);
      toast({
        title: 'Room supprimée',
        description: 'La conversation a été supprimée avec succès',
        variant: 'success',
      });
      navigate('/dashboard');
    } catch (error: any) {
      console.error('Erreur lors de la suppression de la room:', error);
      toast({
        title: 'Erreur',
        description: error.response?.data?.error || 'Erreur lors de la suppression de la room',
        variant: 'destructive',
      });
    } finally {
      setIsDeletingRoom(false);
      setDeleteRoomDialogOpen(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="space-y-4 w-full max-w-md">
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-64 w-full" />
          <Skeleton className="h-20 w-full" />
        </div>
      </div>
    );
  }

  const currentUserMember = members.find((m) => m.id === user?.id);
  const otherMembers = members.filter((m) => m.id !== user?.id);
  const typingUsernames = Array.from(typingMembers)
    .map((id) => members.find((m) => m.id === id)?.username)
    .filter(Boolean);

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-gray-50">
      {/* Sidebar Membres */}
      <div className="w-full md:w-64 bg-white border-r flex flex-col order-2 md:order-1">
        <div className="p-4 border-b">
          <h3 className="font-semibold text-sm">Membres ({members.length}/4)</h3>
        </div>
        <ScrollArea className="flex-1">
          <div className="p-2 space-y-2">
            {currentUserMember && (
              <div className="flex items-center gap-2 p-2 rounded hover:bg-accent">
                <Avatar className="h-8 w-8">
                  <AvatarFallback>
                    {currentUserMember.username.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">
                    {currentUserMember.username} (Vous)
                  </div>
                  {currentUserMember.role && (
                    <div className="text-xs text-muted-foreground truncate">
                      {currentUserMember.role}
                    </div>
                  )}
                </div>
                <div className="h-2 w-2 rounded-full bg-green-500" />
              </div>
            )}
            {otherMembers.map((member) => (
              <div key={member.id} className="flex items-center gap-2 p-2 rounded hover:bg-accent">
                <Avatar className="h-8 w-8">
                  <AvatarFallback>
                    {member.username.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">{member.username}</div>
                  {member.role && (
                    <div className="text-xs text-muted-foreground truncate">
                      {member.role}
                    </div>
                  )}
                </div>
                <div
                  className={`h-2 w-2 rounded-full ${
                    member.isOnline !== false ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col order-1 md:order-2">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              <div className="flex items-center space-x-4">
                <Link to="/dashboard">
                  <ArrowLeft className="h-5 w-5 text-gray-600 hover:text-gray-900" />
                </Link>
                <div>
                  <h1 className="text-xl font-semibold">{room?.name || 'Conversation'}</h1>
                  <p className="text-sm text-gray-500">{members.length} membre(s)</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setInviteModalOpen(true)}
                  disabled={members.length >= 4}
                >
                  <UserPlus className="h-4 w-4 mr-2" />
                  Inviter
                </Button>
                {room?.creator_id === user?.id && (
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => setDeleteRoomDialogOpen(true)}
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Supprimer
                  </Button>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Messages */}
        <ScrollArea className="flex-1">
          <div className="px-4 py-6">
            <div className="max-w-4xl mx-auto space-y-4">
              {messages.map((message) => {
                if (message.status === 'pending_validation' && message.id === pendingMessage?.id) {
                  const validations = message.validations || [];
                  const validationsCount = validations.filter(
                    (v) => v.action !== 'rejected'
                  ).length;
                  const totalMembers = members.filter((m) => m.id !== message.user_id).length;

                  return (
                    <PendingMessageCard
                      key={message.id}
                      message={{
                        ...message,
                        user_id: message.user_id || '',
                      }}
                      currentUserId={user?.id || ''}
                      members={members}
                      validations={validations}
                      validationsCount={validationsCount}
                      totalMembers={totalMembers}
                      socket={socket}
                      onRetract={() => setPendingMessage(null)}
                    />
                  );
                }

                return (
                  <div
                    key={message.id}
                    className={`flex ${message.user_id === user?.id ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[70%] rounded-lg px-4 py-2 ${
                        message.type === 'ai'
                          ? 'bg-blue-50 border border-blue-200'
                          : message.user_id === user?.id
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-white border border-gray-200'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2 mb-1">
                        {message.username && (
                          <div className="text-xs font-semibold">
                            {message.username}
                            {message.role && (
                              <span className="opacity-70"> ({message.role})</span>
                            )}
                          </div>
                        )}
                        {message.user_id === user?.id &&
                          message.status !== 'pending_validation' &&
                          message.type === 'user' && (
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-6 w-6">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end">
                                <DropdownMenuItem
                                  onClick={() => handleEditMessage(message)}
                                >
                                  <Edit className="h-4 w-4 mr-2" />
                                  Éditer
                                </DropdownMenuItem>
                                <DropdownMenuItem
                                  onClick={() => handleDeleteMessage(message.id)}
                                  className="text-destructive"
                                >
                                  <Trash2 className="h-4 w-4 mr-2" />
                                  Supprimer
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          )}
                      </div>
                      {message.type === 'ai' ? (
                        <div className="text-sm prose prose-sm max-w-none dark:prose-invert prose-headings:mt-4 prose-headings:mb-2 prose-p:my-2 prose-ul:my-2 prose-ol:my-2">
                          <ReactMarkdown
                            components={{
                              p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
                              ul: ({ children }) => <ul className="mb-2 ml-4 list-disc space-y-1">{children}</ul>,
                              ol: ({ children }) => <ol className="mb-2 ml-4 list-decimal space-y-1">{children}</ol>,
                              li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                              strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                              em: ({ children }) => <em className="italic">{children}</em>,
                              code: ({ children, className }) => {
                                const isInline = !className;
                                return isInline ? (
                                  <code className="bg-blue-100 dark:bg-blue-900 px-1.5 py-0.5 rounded text-xs font-mono text-blue-800 dark:text-blue-200">
                                    {children}
                                  </code>
                                ) : (
                                  <code className={className}>{children}</code>
                                );
                              },
                              pre: ({ children }) => (
                                <pre className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg overflow-x-auto mb-2 text-xs">
                                  {children}
                                </pre>
                              ),
                              h1: ({ children }) => <h1 className="text-xl font-bold mb-2 mt-4 first:mt-0">{children}</h1>,
                              h2: ({ children }) => <h2 className="text-lg font-bold mb-2 mt-4 first:mt-0">{children}</h2>,
                              h3: ({ children }) => <h3 className="text-base font-bold mb-2 mt-3 first:mt-0">{children}</h3>,
                              blockquote: ({ children }) => (
                                <blockquote className="border-l-4 border-blue-300 dark:border-blue-600 pl-4 italic my-2 text-gray-700 dark:text-gray-300">
                                  {children}
                                </blockquote>
                              ),
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                      )}
                      {message.status === 'rejected' && (
                        <Badge variant="destructive" className="mt-2 text-xs">
                          Rejeté
                        </Badge>
                      )}
                      {message.status === 'error' && (
                        <div className="mt-2">
                          <Badge variant="destructive" className="text-xs mr-2">
                            Erreur
                          </Badge>
                          <Button
                            variant="outline"
                            size="sm"
                            className="text-xs"
                            onClick={() => handleRetryAI(message.id)}
                          >
                            Réessayer
                          </Button>
                        </div>
                      )}
                      {message.edited_at && (
                        <div className="text-xs mt-1 opacity-70">(modifié)</div>
                      )}
                    </div>
                  </div>
                );
              })}
              {typingUsernames.length > 0 && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                    <div className="flex items-center gap-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span className="text-sm text-muted-foreground">
                        {typingUsernames.join(', ')} {typingUsernames.length === 1 ? 'écrit' : 'écrivent'}...
                      </span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </ScrollArea>

        {/* Input */}
        <div className="bg-white border-t p-4">
          <div className="max-w-4xl mx-auto flex space-x-2">
            <Textarea
              className="flex-1 min-h-[60px]"
              placeholder="Tapez votre message..."
              value={messageInput}
              onChange={(e) => {
                setMessageInput(e.target.value);
                handleTyping(e.target.value.length > 0);
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
            />
            <Button onClick={handleSendMessage} disabled={!messageInput.trim()}>
              Envoyer
            </Button>
          </div>
        </div>
      </div>

      {/* Conflict Modal */}
      {conflict && (
        <ConflictVoteModal
          open={!!conflict}
          conflictId={conflict.id}
          messages={conflict.messages}
          votesCount={conflict.votesCount}
          totalMembers={conflict.totalMembers}
          socket={socket}
          onClose={() => setConflict(null)}
        />
      )}

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Éditer le message</DialogTitle>
            <DialogDescription>
              Attention : Éditer ce message supprimera TOUS les messages qui suivent (utilisateurs et IA). Cette action est irréversible.
            </DialogDescription>
          </DialogHeader>
          <Textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            className="min-h-[150px]"
          />
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditDialogOpen(false)}>
              Annuler
            </Button>
            <Button variant="destructive" onClick={handleConfirmEdit}>
              Confirmer et éditer
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Invite Modal */}
      <InviteModal
        open={inviteModalOpen}
        roomId={roomId || ''}
        currentMembers={members.length}
        onClose={() => setInviteModalOpen(false)}
      />

      {/* Role Definition Modal */}
      <RoleDefinitionModal
        open={roleModalOpen}
        roomId={roomId || ''}
        onSuccess={() => {
          setRoleModalOpen(false);
          // Recharger les membres pour avoir le rôle mis à jour
          if (socket && roomId) {
            socket.emit('join-room', roomId);
          }
        }}
      />

      {/* Delete Room Dialog */}
      <Dialog open={deleteRoomDialogOpen} onOpenChange={setDeleteRoomDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Supprimer la conversation</DialogTitle>
            <DialogDescription>
              Êtes-vous sûr de vouloir supprimer cette conversation ? Cette action est irréversible et supprimera tous les messages, membres et données associées.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setDeleteRoomDialogOpen(false)}
              disabled={isDeletingRoom}
            >
              Annuler
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteRoom}
              disabled={isDeletingRoom}
            >
              {isDeletingRoom ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Suppression...
                </>
              ) : (
                'Supprimer'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
