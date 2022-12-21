import { MatButtonModule } from '@angular/material/button';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Document } from '../models';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';

@Component({
  selector: 'app-document',
  templateUrl: './document.component.html',
  styleUrls: ['./document.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: true,
  imports: [MatCardModule, MatDividerModule, MatButtonModule],
})
export class DocumentComponent {
  @Input() document!: Document;
}
