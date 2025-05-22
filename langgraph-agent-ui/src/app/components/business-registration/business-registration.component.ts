import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { BusinessRegistrationRequest } from '../../models/business-registration';

@Component({
  selector: 'app-business-registration',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './business-registration.component.html',
  styleUrls: ['./business-registration.component.css']
})
export class BusinessRegistrationComponent implements OnInit {
  registrationForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.registrationForm = this.fb.group({
      legalName: ['', [Validators.required, Validators.minLength(3)]],
      dbaName: [''],
      address: ['', Validators.required],
      city: ['', Validators.required],
      state: ['', [Validators.required, Validators.maxLength(2)]],
      zipCode: ['', [Validators.required, Validators.pattern(/^\d{5}$/)]],
      businessDescription: ['', [Validators.required, Validators.minLength(20)]],
      ownerEmail: ['', [Validators.required, Validators.email]],
      ownerPhone: ['', [Validators.required, Validators.pattern(/^\d{10}$/)]]
    });
  }

  onSubmit(): void {
    if (this.registrationForm.valid) {
      const formData = this.registrationForm.value as BusinessRegistrationRequest;
      this.apiService.startRegistrationProcess(formData).subscribe({
        next: (response) => console.log('Process started:', response),
        error: (err) => console.error('Submission failed:', err)
      });
    }
  }
}
