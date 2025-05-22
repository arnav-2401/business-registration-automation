import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BusinessRegistrationRequest } from '../models/business-registration';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  startRegistrationProcess(data: BusinessRegistrationRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/start-process`, data);
  }

  getProcessStatus(processId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/status/${processId}`);
  }
}