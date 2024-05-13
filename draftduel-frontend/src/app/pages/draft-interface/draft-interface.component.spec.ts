import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DraftInterfaceComponent } from './draft-interface.component';

describe('DraftInterfaceComponent', () => {
  let component: DraftInterfaceComponent;
  let fixture: ComponentFixture<DraftInterfaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DraftInterfaceComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DraftInterfaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
