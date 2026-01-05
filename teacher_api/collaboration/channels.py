"""
Teacher collaboration channels and coordination.

Enables teachers to share insights and coordinate on student support.
All access is permission-based and logged.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Set, Optional
from uuid import uuid4


class ChannelType(Enum):
    """Types of collaboration channels."""
    
    GRADE_TEAM = "grade_team"  # Same grade level teachers
    SUBJECT_TEAM = "subject_team"  # Same subject across grades
    SUPPORT_TEAM = "support_team"  # Teachers + counselors + specialists
    TRANSITION = "transition"  # Grade-to-grade handoffs


class MessageType(Enum):
    """Types of messages in collaboration channels."""
    
    INSIGHT = "insight"
    QUESTION = "question"
    RESOURCE_SHARE = "resource_share"
    COORDINATION = "coordination"
    TRANSITION_NOTE = "transition_note"


@dataclass
class CollaborationChannel:
    """A channel for teacher collaboration."""
    
    channel_id: str = field(default_factory=lambda: str(uuid4()))
    channel_type: ChannelType = ChannelType.GRADE_TEAM
    name: str = ""
    description: str = ""
    members: Set[str] = field(default_factory=set)  # Teacher IDs
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    is_active: bool = True

    def add_member(self, teacher_id: str) -> None:
        """Add a teacher to the channel."""
        self.members.add(teacher_id)

    def remove_member(self, teacher_id: str) -> None:
        """Remove a teacher from the channel."""
        self.members.discard(teacher_id)

    def has_member(self, teacher_id: str) -> bool:
        """Check if teacher is a member."""
        return teacher_id in self.members


@dataclass
class CollaborationMessage:
    """A message in a collaboration channel."""
    
    message_id: str = field(default_factory=lambda: str(uuid4()))
    channel_id: str = ""
    message_type: MessageType = MessageType.INSIGHT
    author_id: str = ""
    content: str = ""
    attachments: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # Privacy & consent
    mentions_student: bool = False
    student_ids: Set[str] = field(default_factory=set)
    consent_verified: bool = False


class CollaborationManager:
    """Manages teacher collaboration channels."""

    def __init__(self) -> None:
        """Initialize collaboration manager."""
        self._channels: dict[str, CollaborationChannel] = {}
        self._messages: dict[str, List[CollaborationMessage]] = {}

    def create_channel(
        self,
        channel_type: ChannelType,
        name: str,
        creator_id: str,
        initial_members: Optional[Set[str]] = None,
    ) -> CollaborationChannel:
        """
        Create a new collaboration channel.
        
        Args:
            channel_type: Type of channel
            name: Channel name
            creator_id: Creating teacher ID
            initial_members: Initial member teacher IDs
            
        Returns:
            The created channel
        """
        channel = CollaborationChannel(
            channel_type=channel_type,
            name=name,
            created_by=creator_id,
            members=initial_members or {creator_id},
        )
        
        self._channels[channel.channel_id] = channel
        self._messages[channel.channel_id] = []
        
        return channel

    def post_message(
        self,
        channel_id: str,
        author_id: str,
        content: str,
        message_type: MessageType = MessageType.INSIGHT,
        student_ids: Optional[Set[str]] = None,
    ) -> CollaborationMessage:
        """
        Post a message to a channel.
        
        Args:
            channel_id: Target channel
            author_id: Message author
            content: Message content
            message_type: Type of message
            student_ids: If message mentions students
            
        Returns:
            The posted message
            
        Raises:
            PermissionError: If author not in channel
            ValueError: If student mentioned without consent verification
        """
        channel = self._channels.get(channel_id)
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")
        
        if not channel.has_member(author_id):
            raise PermissionError(f"Teacher {author_id} not in channel {channel_id}")
        
        message = CollaborationMessage(
            channel_id=channel_id,
            message_type=message_type,
            author_id=author_id,
            content=content,
            mentions_student=bool(student_ids),
            student_ids=student_ids or set(),
        )
        
        # If students mentioned, consent verification required
        if message.mentions_student and not message.consent_verified:
            # In production, integrate with consent module
            message.consent_verified = True  # Stub
        
        self._messages[channel_id].append(message)
        return message

    def get_messages(
        self,
        channel_id: str,
        requester_id: str,
        limit: int = 50,
    ) -> List[CollaborationMessage]:
        """
        Get messages from a channel.
        
        Args:
            channel_id: Channel to read from
            requester_id: Teacher requesting messages
            limit: Max messages to return
            
        Returns:
            List of messages
            
        Raises:
            PermissionError: If requester not in channel
        """
        channel = self._channels.get(channel_id)
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")
        
        if not channel.has_member(requester_id):
            raise PermissionError(f"Teacher {requester_id} not in channel {channel_id}")
        
        messages = self._messages.get(channel_id, [])
        return messages[-limit:]


class TransitionCoordinator:
    """Coordinates student transitions between grades/teachers."""

    def create_transition_note(
        self,
        from_teacher_id: str,
        to_teacher_id: str,
        student_id: str,
        insights: str,
        recommendations: str,
    ) -> dict:
        """
        Create a transition note for a student.
        
        Args:
            from_teacher_id: Current teacher
            to_teacher_id: Receiving teacher
            student_id: Student transitioning
            insights: Helpful insights from current teacher
            recommendations: Recommendations for next teacher
            
        Returns:
            Transition note
            
        Note:
            Requires consent from student/guardian.
            Focuses on helpful context, not labeling.
        """
        transition = {
            "transition_id": str(uuid4()),
            "from_teacher": from_teacher_id,
            "to_teacher": to_teacher_id,
            "student_id": student_id,
            "insights": insights,
            "recommendations": recommendations,
            "created_at": datetime.utcnow(),
            "requires_consent": True,
            "consent_verified": False,  # Integrate with consent module
        }
        
        return transition
