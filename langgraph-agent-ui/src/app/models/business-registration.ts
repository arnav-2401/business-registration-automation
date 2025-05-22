export interface BusinessRegistrationRequest {
    legalName: string;
    dbaName?: string;
    address: string;
    city: string;
    state: string;
    zipCode: string;
    businessDescription: string;
    ownerEmail: string;
    ownerPhone: string;
}
  
export interface WorkflowState {
    status: 'idle' | 'processing' | 'completed' | 'error';
    currentStep?: string;
    confirmationNumber?: string;
    errors?: string[];
}