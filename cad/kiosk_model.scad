// ====================================================================
// BITTU XEROX 24/7 SMART SELF-SERVICE KIOSK - 3D PARAMETRIC OPENSCAD MODEL
// Fully Aligned Mechanical Assembly (Engineered Clearances & Thermal Ducting)
// ====================================================================
// Instructions: Open in OpenSCAD and press [F5] to Preview or [F6] to Render.

$fn = 36;

// ==========================================
// 1. CONFIGURATION & TOGGLES
// ==========================================
view_mode            = "side_by_side"; // "side_by_side", "assembled", "internals_only", "shell_only"
include_phys_buttons = false;          // Clean 100% Touchscreen UI
show_labels          = true;           // 3D Callout Badges

// BIG 15.6" FULL HD WIDESCREEN DISPLAY (420mm W x 260mm H)
screen_w = 420;
screen_h = 260;

// Overall Cabinet Envelope (Millimeters)
kiosk_w = 600;   // Overall Width (X)
kiosk_d = 600;   // Overall Depth (Y)
kiosk_h = 1650;  // Overall Height (Z)
wall_t  = 12;    // 12mm MDF Panels

// Colors
col_side_yellow  = [0.93, 0.77, 0.18, 1.00]; // Golden Yellow Side Walls
col_front_green  = [0.00, 0.52, 0.24, 1.00]; // Rich Forest Green Front
col_top_dark     = [0.12, 0.16, 0.18, 1.00]; // Charcoal Black Canopy
col_shelf_green  = [0.10, 0.65, 0.32, 1.00]; // Green 12mm MDF Shelves
col_pine_wood    = [0.85, 0.75, 0.60, 1.00]; // Pine Frame Posts & Cleats
col_hardware_blk = [0.12, 0.12, 0.14, 1.00]; // Matte Black Hardware
col_brand_gold   = [1.00, 0.85, 0.20, 1.00]; // Gold Branding Text & Locator Brackets
col_metal_chrome = [0.85, 0.88, 0.90, 1.00]; // Chrome Cam Locks & Screws
col_glass_screen = [0.08, 0.12, 0.16, 1.00]; // Deep Black Glass Bezel
col_active_ui    = [0.12, 0.48, 0.38, 0.95]; // Glowing Touch UI

// ==========================================
// 2. MAIN SCENE CONTROLLER
// ==========================================
if (view_mode == "side_by_side") {
    // Left: Fully Aligned Internal Hardware Stack
    translate([-750, 0, 0]) {
        internal_hardware_assembly();
        if (show_labels) callout_labels_internal();
    }
    // Right: Clean Sleek External Enclosure
    translate([0, 0, 0]) {
        external_kiosk_enclosure();
        big_touchscreen_display_unit();
    }
} else if (view_mode == "assembled") {
    internal_hardware_assembly();
    external_kiosk_enclosure();
    big_touchscreen_display_unit();
    if (show_labels) callout_labels_internal();
} else if (view_mode == "internals_only") {
    internal_hardware_assembly();
    big_touchscreen_display_unit();
    if (show_labels) callout_labels_internal();
} else if (view_mode == "shell_only") {
    external_kiosk_enclosure();
    big_touchscreen_display_unit();
}

// ==========================================
// 3. BIG 15.6" TOUCHSCREEN DISPLAY UNIT
// ==========================================
module big_touchscreen_display_unit() {
    translate([kiosk_w/2 - screen_w/2, -3, 1040]) {
        // Deep Black Bezel Outer Frame
        color(col_glass_screen) {
            cube([screen_w, 16, screen_h]);
        }
        // Glowing Active Touch Display Surface
        color(col_active_ui) {
            translate([12, -2, 12])
                cube([screen_w - 24, 3, screen_h - 24]);
        }
    }
    // Gold Chamfered Bezel Surround
    color(col_brand_gold) {
        translate([kiosk_w/2 - screen_w/2 - 4, -5, 1040 - 4])
            difference() {
                cube([screen_w + 8, 4, screen_h + 8]);
                translate([4, -1, 4]) cube([screen_w, 6, screen_h]);
            }
    }
}

// ==========================================
// 4. EXTERNAL CABINET ENCLOSURE
// ==========================================
module external_kiosk_enclosure() {
    // A. GOLDEN YELLOW SIDE PANELS
    color(col_side_yellow) {
        translate([0, 0, 0]) side_profile_wall();
        translate([kiosk_w - wall_t, 0, 0]) side_profile_wall();
    }

    // B. CLEAN TOP CANOPY MARQUEE (NO FRONT MESH)
    color(col_top_dark) {
        translate([wall_t, 0, 1350])
            cube([kiosk_w - 2*wall_t, wall_t, 300]);
        translate([0, 0, kiosk_h - wall_t])
            cube([kiosk_w, kiosk_d, wall_t]);
    }

    // Top Canopy Gold Branding
    color(col_brand_gold) {
        translate([kiosk_w/2, -3, 1540])
            rotate([90, 0, 0])
            linear_extrude(2)
            text("Bittu", size=42, font="Liberation Sans:style=Bold Italic", halign="center");

        translate([kiosk_w/2, -3, 1490])
            rotate([90, 0, 0])
            linear_extrude(2)
            text("24/7 XEROX KIOSK", size=18, font="Liberation Sans:style=Bold", halign="center");

        translate([kiosk_w/2, -3, 1450])
            rotate([90, 0, 0])
            linear_extrude(2)
            text("SMART CAMPUS PRINTING HUB", size=11, font="Liberation Sans:style=Bold", halign="center");
    }

    // C. FRONT FOREST GREEN FASCIA (WITH PRECISION CUTOUTS)
    color(col_front_green) {
        difference() {
            // Front Green Panel (Z = 0 to 1350mm)
            translate([wall_t, 0, 0])
                cube([kiosk_w - 2*wall_t, wall_t, 1350]);

            // 1. Big 15.6" Screen Window Cutout
            translate([kiosk_w/2 - screen_w/2 - 2, -5, 1040 - 2])
                cube([screen_w + 4, wall_t + 10, screen_h + 4]);

            // 2. Document Retrieval Chute Cutout (Aligned with Printer Chute)
            translate([80, -5, 525])
                cube([kiosk_w - 160, wall_t + 10, 65]);
        }
    }

    // D. ERGONOMIC SLOPED PHONE STAGING DOCK (Z = 830 to 1020mm)
    color(col_front_green) {
        translate([wall_t, -60, 830])
            rotate([38.66, 0, 0])
            cube([kiosk_w - 2*wall_t, 280, wall_t]);
    }
    // Silicone Phone Staging Pad
    color([0.15, 0.18, 0.20]) {
        translate([kiosk_w/2 - 160, -45, 870])
            rotate([38.66, 0, 0])
            cube([320, 160, 6]);
    }

    // E. FRONT GRAPHICS & QR BOX
    color([0.88, 0.88, 0.90]) {
        translate([kiosk_w/2 - 50, -2, 700]) cube([100, 3, 100]);
    }
    color([0.1, 0.1, 0.1]) {
        translate([kiosk_w/2 - 40, -4, 710]) cube([80, 4, 80]);
    }
    color([0.95, 0.95, 0.95]) {
        translate([kiosk_w/2, -2, 665])
            rotate([90, 0, 0])
            linear_extrude(2)
            text("SCAN TO BEGIN OR VISIT APP.BITTUXEROX.IN", size=10, font="Liberation Sans:style=Bold", halign="center");
    }

    // Three Bottom Workflow Step Badges: [03 PRINT] [02 UPLOAD] [01 SCAN]
    color([0.95, 0.95, 0.95]) {
        for (b_info = [[60, "03", "PRINT"], [235, "02", "UPLOAD"], [410, "01", "SCAN"]]) {
            translate([b_info[0], -2, 420]) {
                difference() {
                    cube([130, 3, 75]);
                    translate([5, -1, 5]) cube([120, 5, 65]);
                }
            }
            translate([b_info[0] + 65, -4, 465])
                rotate([90, 0, 0]) linear_extrude(2)
                text(b_info[1], size=16, font="Liberation Sans:style=Bold", halign="center");
            translate([b_info[0] + 65, -4, 435])
                rotate([90, 0, 0]) linear_extrude(2)
                text(b_info[2], size=10, font="Liberation Sans:style=Bold", halign="center");
        }
    }

    // Bottom Positive-Pressure Intake Louvers
    color([0.05, 0.05, 0.05]) {
        for (l_z = [140, 180, 220]) {
            translate([75, -2, l_z])  cube([110, 4, 12]);
            translate([245, -2, l_z]) cube([110, 4, 12]);
            translate([415, -2, l_z]) cube([110, 4, 12]);
        }
    }

    // F. REAR WALL WITH CIRCULAR 120mm FAN CUTOUTS & EXHAUST LOUVERS
    color(col_front_green) {
        difference() {
            // Full Rear Panel
            translate([wall_t, kiosk_d - wall_t, 0])
                cube([kiosk_w - 2*wall_t, wall_t, kiosk_h]);

            // DUAL 120mm FAN CIRCULAR CUTOUT HOLES (Left & Right Chimney)
            translate([140, kiosk_d - wall_t - 2, 1500])
                rotate([-90, 0, 0]) cylinder(r=58, h=wall_t + 10);

            translate([kiosk_w - 140, kiosk_d - wall_t - 2, 1500])
                rotate([-90, 0, 0]) cylinder(r=58, h=wall_t + 10);

            // Lower AC Power Inlet IEC Cutout (Bottom Right)
            translate([kiosk_w - wall_t - 80, kiosk_d - wall_t - 2, 30])
                cube([60, wall_t + 10, 40]);
        }
    }
    // Rear Fan Protective Metal Finger Grilles
    color(col_metal_chrome) {
        translate([140, kiosk_d + 1, 1500]) rotate([-90, 0, 0]) {
            difference() { cylinder(r=62, h=2); cylinder(r=56, h=4); }
            cube([120, 2, 2], center=true);
            cube([2, 120, 2], center=true);
        }
        translate([kiosk_w - 140, kiosk_d + 1, 1500]) rotate([-90, 0, 0]) {
            difference() { cylinder(r=62, h=2); cylinder(r=56, h=4); }
            cube([120, 2, 2], center=true);
            cube([2, 120, 2], center=true);
        }
    }
}

// Side Profile Wall Geometry
module side_profile_wall() {
    rotate([90, 0, 90])
    linear_extrude(height = wall_t) {
        polygon(points = [
            [0, 0],
            [kiosk_d, 0],
            [kiosk_d, kiosk_h],
            [0, kiosk_h],
            [0, 1180],
            [-60, 880],
            [0, 820],
            [0, 0]
        ]);
    }
}

// ==========================================
// 5. PERFECTLY ALIGNED INTERNAL HARDWARE STACK
// ==========================================
module internal_hardware_assembly() {
    // -----------------------------------------
    // A. 4 PINE CORNER POSTS (Full Height)
    // -----------------------------------------
    color(col_pine_wood) {
        for (px = [wall_t, kiosk_w - wall_t - 25]) {
            for (py = [wall_t, kiosk_d - wall_t - 25]) {
                translate([px, py, 0]) cube([25, 25, kiosk_h - 20]);
            }
        }
    }

    // -----------------------------------------
    // B. 5 GREEN MDF SHELVES (Exact Z-Elevations)
    // -----------------------------------------
    color(col_shelf_green) {
        // Shelf 1: Base Floor (Z = 24mm)
        translate([wall_t, wall_t, 24])   cube([kiosk_w - 2*wall_t, kiosk_d - 2*wall_t, wall_t]);
        // Shelf 2: Paper Reserve (Left, Z = 250mm)
        translate([wall_t, wall_t, 250])  cube([320, kiosk_d - 2*wall_t - 50, wall_t]);
        // Shelf 3: Heavy Printer Shelf (Z = 510mm)
        translate([wall_t, wall_t, 510])  cube([kiosk_w - 2*wall_t, kiosk_d - 2*wall_t - 30, wall_t]);
        // Shelf 4: Scanner Shelf (Z = 760mm)
        translate([wall_t, wall_t, 760])  cube([kiosk_w - 2*wall_t, kiosk_d - 2*wall_t - 30, wall_t]);
        // Shelf 5: Top Electronics & Pi 5 Shelf (Z = 1000mm)
        translate([wall_t, wall_t + 50, 1000]) cube([kiosk_w - 2*wall_t, kiosk_d - 2*wall_t - 80, wall_t]);
    }

    // -----------------------------------------
    // C. DUAL 120mm PWM EXHAUST FANS (FLUSH-MOUNTED TO REAR WALL)
    // -----------------------------------------
    color(col_hardware_blk) {
        // Left Chimney Fan (Z=1500mm, Y=563mm - flush with rear wall)
        translate([140, kiosk_d - wall_t - 25, 1500]) {
            rotate([-90, 0, 0]) {
                difference() {
                    cube([120, 120, 25], center=true); // 120x120x25mm Fan Housing
                    cylinder(r=56, h=30, center=true);
                }
                // Central Fan Hub & 7 Impeller Blades
                color([0.2, 0.2, 0.25]) cylinder(r=20, h=22, center=true);
            }
        }

        // Right Chimney Fan
        translate([kiosk_w - 140, kiosk_d - wall_t - 25, 1500]) {
            rotate([-90, 0, 0]) {
                difference() {
                    cube([120, 120, 25], center=true);
                    cylinder(r=56, h=30, center=true);
                }
                color([0.2, 0.2, 0.25]) cylinder(r=20, h=22, center=true);
            }
        }
    }

    // -----------------------------------------
    // D. SCANNER BAY (Z = 760 to 830mm - 120mm Clearance)
    // -----------------------------------------
    // Canon LiDE 300 Flatbed Scanner (Centrally Seated)
    color([0.16, 0.16, 0.18]) {
        translate([kiosk_w/2 - 235, 60, 772]) {
            cube([470, 370, 42]); // Scanner Body
            // Glass Platen
            color([0.35, 0.75, 0.90, 0.5]) translate([40, 40, 40]) cube([390, 280, 3]);
        }
    }

    // -----------------------------------------
    // E. PRINTER & GRAVITY OUTPUT RETRIEVAL CHUTE (Z = 510 to 740mm)
    // -----------------------------------------
    // Brother HL-L2321D Laser Printer
    color(col_hardware_blk) {
        translate([kiosk_w/2 - 245, 80, 522]) {
            cube([490, 400, 210]); // Printer Main Chassis
            // Front Paper Input Drawer (250 sheets)
            translate([30, -20, 10]) cube([430, 20, 55]);
        }
    }
    // 4 3D-Printed Yellow Corner Locator Brackets
    color(col_brand_gold) {
        translate([50, 76, 522])    cube([22, 22, 35]);
        translate([528, 76, 522])   cube([22, 22, 35]);
        translate([50, 458, 522])   cube([22, 22, 35]);
        translate([528, 458, 522])  cube([22, 22, 35]);
    }
    // Smooth Gravity Print Output Chute (Slopes directly from printer mouth to front retrieval slot)
    color(col_brand_gold) {
        translate([kiosk_w/2 - 210, 20, 535])
            rotate([12, 0, 0])
            cube([420, 140, 8]);
    }

    // -----------------------------------------
    // F. LOWER COMPARTMENT POWER & PAPER STORAGE (Z = 24 to 500mm)
    // -----------------------------------------
    // 1. 600VA Line-Interactive UPS Battery (Bottom Left)
    color(col_hardware_blk) {
        translate([50, 80, 36]) cube([160, 280, 180]);
    }
    // 2. AC Surge Protection Board & MCB Box & Modbus Energy Meter
    color([0.85, 0.85, 0.88]) translate([170, 30, 36]) cube([65, 130, 42]);
    color([0.95, 0.95, 0.98]) translate([250, 40, 36]) cube([55, 75, 80]);
    color([0.70, 0.72, 0.75]) translate([250, 150, 36]) cube([65, 85, 90]);

    // 3. 1,500 Sheets A4 Paper Reserve (Left Shelf Z=262mm)
    color([0.97, 0.97, 0.97]) translate([50, 70, 262]) cube([260, 320, 145]);
    color([0.85, 0.15, 0.15]) translate([48, 200, 262]) cube([264, 40, 147]);

    // 4. Waste Collection Bin (Right Side)
    color([0.22, 0.22, 0.25]) translate([350, 60, 36]) cube([180, 320, 444]);

    // -----------------------------------------
    // G. UPPER ELECTRONICS (Z = 1000 to 1450mm)
    // -----------------------------------------
    // Raspberry Pi 5 + Active Cooler + 27W Power Supply (On Shelf Z=1012mm)
    color([0.10, 0.55, 0.25]) translate([340, 180, 1012]) cube([85, 56, 18]);
    color([0.78, 0.80, 0.84]) translate([360, 195, 1030]) cube([45, 40, 12]);
    color([0.95, 0.95, 0.95]) translate([460, 180, 1012]) cube([45, 70, 35]);
    color([0.2, 0.2, 0.22]) translate([kiosk_w/2 - 90, 180, 1012]) cube([110, 45, 20]);
    color([0.1, 0.1, 0.1]) translate([kiosk_w/2 + 40, 200, 1012]) cylinder(r=8, h=10);

    // PIR Sensors on console edge
    for (pir_x = [40, 510]) {
        color([0.0, 0.4, 0.7]) translate([pir_x, 30, 880]) cube([36, 14, 36]);
        color([0.95, 0.95, 0.98]) translate([pir_x + 18, 24, 898]) sphere(r=11);
    }
}

// ==========================================
// 6. 3D CALLOUT LABELS
// ==========================================
module callout_labels_internal() {
    color([1.0, 1.0, 1.0]) {
        translate([kiosk_w/2, 20, 1450]) render_tag("REAR DUAL 120mm PWM EXHAUST FANS");
        translate([kiosk_w/2, 20, 1330]) render_tag("BIG 15.6\" FHD WIDESCREEN DISPLAY");
        translate([kiosk_w/2 + 100, 150, 1080]) render_tag("PI 5 + COOLER + 27W PSU");
        translate([kiosk_w/2, 0, 790]) render_tag("CANON LiDE 300 SCANNER");
        translate([kiosk_w/2, 0, 600]) render_tag("BROTHER PRINTER + OUTPUT CHUTE");
        translate([100, 0, 380]) render_tag("1,500 SHEETS A4 PAPER RESERVE");
        translate([40, 0, 180]) render_tag("600VA ONLINE UPS POWER");
        translate([270, 0, 120]) render_tag("MODBUS METER + MCB BOX");
        translate([450, 0, 420]) render_tag("WASTE COLLECTION BIN");
    }
}

module render_tag(txt) {
    rotate([90, 0, 0]) {
        linear_extrude(height = 1)
            text(txt, size = 12, font = "Liberation Sans:style=Bold", halign = "center");
    }
}
