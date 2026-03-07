export type SessionType = 'Deep Work' | 'Creative Sprint' | 'Planning' | 'Learning';

export type SessionDraft = {
  goal: string;
  type: SessionType;
  duration: number;
  why: string;
  task: string;
};

export type SessionResult = {
  completed: boolean;
  distractions: number;
  reflection: string;
  focusScore: number;
  timestamp: string;
};

export type StoredSession = SessionDraft & SessionResult;
