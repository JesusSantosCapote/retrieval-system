import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Document } from '../models';

@Component({
  selector: 'app-document',
  templateUrl: './document.component.html',
  styleUrls: ['./document.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: true,
})
export class DocumentComponent {
  @Input() document!: Document;
}
