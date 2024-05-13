import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmptyRosterEntryComponent } from './empty-roster-entry.component';

describe('EmptyRosterEntryComponent', () => {
  let component: EmptyRosterEntryComponent;
  let fixture: ComponentFixture<EmptyRosterEntryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmptyRosterEntryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmptyRosterEntryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
