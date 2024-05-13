import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RosterEntryComponent } from './roster-entry.component';

describe('RosterEntryComponent', () => {
  let component: RosterEntryComponent;
  let fixture: ComponentFixture<RosterEntryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RosterEntryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RosterEntryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
