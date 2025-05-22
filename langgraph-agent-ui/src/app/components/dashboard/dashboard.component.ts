import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebsocketService } from '../../services/websocket.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  statusUpdates: string[] = [];
  currentStatus: string = 'idle';

  constructor(private wsService: WebsocketService) {}

  ngOnInit() {
    this.wsService.connect().subscribe({
      next: (update: any) => {
        this.statusUpdates.push(update.message);
        this.currentStatus = update.status;
      },
      error: (err) => console.error('WebSocket error:', err)
    });
  }
}