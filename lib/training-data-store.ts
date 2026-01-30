export interface TrainingFile {
  id: string
  name: string
  type: string
  size: number
  uploadedAt: string
}

export const TrainingDataStore = {
  files: [] as TrainingFile[],

  getFiles: (): TrainingFile[] => {
    return TrainingDataStore.files
  },

  addFile: (file: TrainingFile): void => {
    TrainingDataStore.files.push(file)
  },

  removeFile: (id: string): void => {
    TrainingDataStore.files = TrainingDataStore.files.filter((f) => f.id !== id)
  },

  clearFiles: (): void => {
    TrainingDataStore.files = []
  },
}
