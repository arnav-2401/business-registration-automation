import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket$!: WebSocketSubject<any>;

  connect(processId?: string): WebSocketSubject<any> {
    const url = processId 
      ? `ws://localhost:5000/ws/${processId}`
      : 'ws://localhost:5000/ws';
    this.socket$ = webSocket(url);
    return this.socket$;
  }

  disconnect() {
    if (this.socket$) {
      this.socket$.complete();
    }
  }
}