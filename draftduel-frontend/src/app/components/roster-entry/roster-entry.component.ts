import { Component, Input } from '@angular/core';
import { Player } from '../../services/stats.service';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-roster-entry',
  standalone: true,
  imports: [NgIf],
  templateUrl: './roster-entry.component.html',
  styleUrl: './roster-entry.component.scss',
})
export class RosterEntryComponent {
  @Input() player!: Player;
}
