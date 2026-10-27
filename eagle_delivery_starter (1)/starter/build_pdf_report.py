import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Header (pages 2 and 3)
        if self._pageNumber > 1:
            self.drawString(36, 11 * 72 - 28, "COSC 461/561 Project 1: Eagle Delivery Report — Anurag Singh Rawat (EMU)")
            self.setStrokeColor(colors.HexColor("#cccccc"))
            self.setLineWidth(0.5)
            self.line(36, 11 * 72 - 32, 8.5 * 72 - 36, 11 * 72 - 32)
            
        # Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 36, 22, page_str)
        self.drawString(36, 22, "Eastern Michigan University — Department of Computer Science")
        self.setStrokeColor(colors.HexColor("#cccccc"))
        self.setLineWidth(0.5)
        self.line(36, 30, 8.5 * 72 - 36, 30)
        
        self.restoreState()


def build_pdf():
    pdf_filename = "Eagle_Delivery_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#002b49'),
        alignment=1, # Center
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#333333'),
        alignment=1,
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#005580'),
        alignment=1,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#002b49'),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#222222'),
        spaceBefore=3,
        spaceAfter=1,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.3,
        leading=10.4,
        textColor=colors.HexColor('#111111'),
        alignment=4, # Justified
        spaceAfter=2.5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.1,
        leading=9.8,
        textColor=colors.HexColor('#111111'),
        leftIndent=10,
        spaceAfter=1.5
    )

    math_box_style = ParagraphStyle(
        'MathBox',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.3,
        leading=10.5,
        alignment=1,
        textColor=colors.HexColor('#002244'),
        spaceBefore=2,
        spaceAfter=2
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=8.8,
        alignment=1
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=8.8,
        alignment=1
    )

    table_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=8.8,
        alignment=0
    )

    table_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.white,
        alignment=1
    )

    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.HexColor('#444444'),
        alignment=1,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.0,
        leading=10.0,
        textColor=colors.HexColor('#002b49'),
        leftIndent=8,
        rightIndent=8,
        spaceBefore=2,
        spaceAfter=2
    )

    story = []

    # =========================================================================
    # PAGE 1: Title, Problem Formulation, Admissibility Proof
    # =========================================================================
    story.append(Paragraph("COSC 461/561 Project 1: Eagle Delivery Report", title_style))
    story.append(Paragraph("Autonomous Campus Navigation via Classical Heuristic Search and Q-Learning", subtitle_style))
    story.append(Paragraph("Author: Anurag Singh Rawat &nbsp;|&nbsp; Eastern Michigan University (EMU) &nbsp;|&nbsp; Date: October 26, 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#002b49"), spaceBefore=1, spaceAfter=4))

    story.append(Paragraph("1. Introduction & Formal Problem Formulation", h1_style))
    story.append(Paragraph(
        "Autonomous mobile delivery robotics requires robust decision-making across both structured planning and unknown environment learning. "
        "The <b>Eagle Delivery</b> project simulates a delivery robot operating across the Eastern Michigan University campus. The robot's mission is "
        "to transport parcels between building entrances on discrete 2D grid campus layouts composed of traversable walkways and impassable buildings. "
        "We implement and evaluate two core AI paradigms: (1) <i>Informed & Uninformed Classical Search</i> (BFS and A* with Manhattan distance) "
        "under known deterministic maps, and (2) <i>Model-Free Reinforcement Learning</i> (tabular Q-learning with &epsilon;-greedy exploration) "
        "to synthesize optimal navigation policies purely through interactive experience.",
        body_style
    ))
    story.append(Paragraph("We formally define the campus navigation problem as a discrete state-space planning model:", body_style))
    story.append(Paragraph("&bull; <b>State Space (<i>S</i>):</b> 2D discrete grid coordinates <i>s = (r, c)</i> representing traversable walkways ('.') and building entrances ('S, L, H, D, P, W'). For an <i>R &times; C</i> campus grid, <i>S</i> contains all non-wall coordinates: <i>(r, c) &in; {0, ..., R-1} &times; {0, ..., C-1}</i> such that <i>map(r, c) &ne; '#'</i>.", bullet_style))
    story.append(Paragraph("&bull; <b>Initial State (<i>s<sub>0</sub></i>):</b> The grid coordinate <i>(r<sub>0</sub>, c<sub>0</sub>) &in; S</i> of the package pickup entrance (e.g., Student Center <i>S = (1, 1)</i>).", bullet_style))
    story.append(Paragraph("&bull; <b>Action Space (<i>A</i>):</b> Four discrete cardinal moves: <i>A = {UP, DOWN, LEFT, RIGHT}</i> with coordinate displacements &Delta;(<i>a</i>) &in; {(-1,0), (1,0), (0,-1), (0,1)}. Diagonal movements are strictly prohibited.", bullet_style))
    story.append(Paragraph("&bull; <b>Transition Model (<i>T: S &times; A &rarr; S</i>):</b> Deterministic transition <i>T(s, a) = s' = s + &Delta;(a)</i> if <i>s'</i> is within grid boundaries and traversable. If an action targets an impassable building obstacle ('#') or boundary wall, the robot collides and remains in its current state: <i>T(s, a) = s</i>.", bullet_style))
    story.append(Paragraph("&bull; <b>Goal Test (<i>G(s)</i>):</b> A predicate checking if <i>s = (r<sub>g</sub>, c<sub>g</sub>)</i>, the designated delivery building entrance. Intermediate building letters along the route remain traversable and do not terminate the episode.", bullet_style))
    story.append(Paragraph("&bull; <b>Path Cost (<i>c(s, a, s')</i>):</b> Every attempted action incurs a uniform unit cost of <i>c = 1</i>, regardless of movement success. The total path cost for a trajectory &pi; = (s<sub>0</sub>, ..., s<sub>k</sub>) is the total step count: <i>Cost(&pi;) = len(&pi;) - 1 = k</i>.", bullet_style))
    story.append(Paragraph("&bull; <b>Optimality of Breadth-First Search (BFS):</b> In graphs where all step costs are positive and uniform (<i>c = 1</i>), BFS expands states in strictly non-decreasing order of path cost (depth levels). By maintaining a FIFO queue, all states at depth <i>d</i> are fully expanded before any state at depth <i>d+1</i> is popped. When BFS first pops the goal state from the frontier, the discovered path is mathematically guaranteed to possess minimal steps, ensuring path cost optimality.", bullet_style))

    story.append(Paragraph("2. Heuristic Admissibility Proof for Manhattan Distance", h1_style))
    story.append(Paragraph(
        "For informed search (Part A), the Manhattan distance (<i>L<sub>1</sub></i> norm / taxicab distance) heuristic between the current position "
        "<i>s = (r<sub>s</sub>, c<sub>s</sub>)</i> and destination building <i>g = (r<sub>g</sub>, c<sub>g</sub>)</i> is computed as:",
        body_style
    ))
    story.append(Paragraph("<i>h(s) = |r<sub>s</sub> - r<sub>g</sub>| + |c<sub>s</sub> - c<sub>g</sub>|</i>", math_box_style))

    story.append(Paragraph("<b>Formal Definition of Admissibility:</b> A search heuristic <i>h(s)</i> is admissible if it never overestimates the true minimal cost <i>h<sup>*</sup>(s)</i> required to reach the goal from state <i>s</i>: &nbsp; &forall; <i>s &in; S, &nbsp; 0 &le; h(s) &le; h<sup>*</sup>(s)</i>.", body_style))
    
    story.append(Paragraph("<b>Mathematical Proof:</b>", h2_style))
    story.append(Paragraph(
        "<b>1. Relaxed Problem Formulation:</b> Consider a relaxed abstraction of the grid environment wherein all campus building walls and obstacle cells ('#') are removed, leaving an open 4-connected 2D grid on <b>Z</b><sup>2</sup>.<br/>"
        "<b>2. Minimum Coordinate Displacements:</b> To reach coordinate <i>(r<sub>g</sub>, c<sub>g</sub>)</i> from <i>(r<sub>s</sub>, c<sub>s</sub>)</i>, the agent must displace its vertical coordinate by exactly <i>|r<sub>s</sub> - r<sub>g</sub>|</i> and its horizontal coordinate by <i>|c<sub>s</sub> - c<sub>g</sub>|</i>. "
        "At every step <i>t</i>, the robot can select only one cardinal action, changing at most one coordinate by at most one unit: <i>|&Delta;r<sub>t</sub>| + |&Delta;c<sub>t</sub>| &le; 1</i>. "
        "Summing displacements over any arbitrary <i>k</i>-step valid trajectory to the goal:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>|r<sub>s</sub> - r<sub>g</sub>| &le; &sum;<sub>t=1</sub><sup>k</sup> |&Delta;r<sub>t</sub>|</i> &nbsp;&nbsp;and&nbsp;&nbsp; "
        "<i>|c<sub>s</sub> - c<sub>g</sub>| &le; &sum;<sub>t=1</sub><sup>k</sup> |&Delta;c<sub>t</sub>|</i><br/>"
        "Adding these two geometric inequalities yields:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>|r<sub>s</sub> - r<sub>g</sub>| + |c<sub>s</sub> - c<sub>g</sub>| &le; &sum;<sub>t=1</sub><sup>k</sup> ( |&Delta;r<sub>t</sub>| + |&Delta;c<sub>t</sub>| ) &le; &sum;<sub>t=1</sub><sup>k</sup> 1 = k</i><br/>"
        "Therefore, no valid sequence of cardinal moves can bridge the coordinate gap in fewer than <i>|r<sub>s</sub> - r<sub>g</sub>| + |c<sub>s</sub> - c<sub>g</sub>|</i> steps. "
        "The minimal path cost in the unconstrained relaxed problem is precisely <i>h<sup>*</sup><sub>relaxed</sub>(s) = h(s)</i>.<br/>"
        "<b>3. Impact of Campus Obstacles:</b> In the actual environment, impassable building walls ('#') constrain traversable walkways. "
        "Introducing obstacles can only restrict available paths or force detours; obstacles cannot create shortcuts or enable diagonal transitions. Hence:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>h<sup>*</sup>(s) &ge; h<sup>*</sup><sub>relaxed</sub>(s) = h(s)</i><br/>"
        "4. Consistency (Monotonicity): By the triangle inequality on <i>L<sub>1</sub></i>, for any adjacent states <i>s, s'</i> with step cost <i>c(s, a, s') = 1</i>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>|h(s) - h(s')| &le; |r<sub>s</sub> - r<sub>s'</sub>| + |c<sub>s</sub> - c<sub>s'</sub>| = 1 = c(s, a, s') &nbsp;&rArr;&nbsp; h(s) &le; c(s, a, s') + h(s')</i><br/>"
        "Because <i>h(s) &le; h<sup>*</sup>(s)</i> everywhere and <i>h(goal) = 0</i>, the Manhattan distance heuristic is strictly admissible and consistent. "
        "Consequently, A* graph search is mathematically guaranteed to return a cost-optimal path without needing to reopen closed nodes. &#9632;",
        body_style
    ))

    # Page break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Part A Search Experiments, 6-Row Table, Figure 1, Analysis
    # =========================================================================
    story.append(Paragraph("3. Part A: Heuristic Search Implementation & Empirical Evaluation", h1_style))
    story.append(Paragraph(
        "We implemented BFS and A* in <code>agents.py</code>. Our A* implementation utilizes Python's <code>heapq</code> with entries "
        "structured as <code>(f, insertion_order, g, state)</code>, where <i>f(s) = g(s) + h(s)</i>. A monotonic integer counter breaks "
        "<i>f</i>-ties in strict FIFO order without comparing coordinate tuples. A <code>best_g</code> lookup table tracks the minimal cost "
        "discovered to each state, lazily skipping stale queue entries whose stored <i>g</i> exceeds <code>best_g[state]</code>. "
        "Successors are expanded in the required order: <code>UP, DOWN, LEFT, RIGHT</code>.",
        body_style
    ))

    # Table 1: Six Search Comparisons
    story.append(Paragraph("<b>Table 1: Six Required BFS vs. A* Empirical Comparisons Across Baseline and Detour Maps</b>", h2_style))
    
    t1_data = [
        [Paragraph("Map Environment", table_hdr_style),
         Paragraph("Delivery Task", table_hdr_style),
         Paragraph("BFS Route Length", table_hdr_style),
         Paragraph("A* Route Length", table_hdr_style),
         Paragraph("BFS Expansions", table_hdr_style),
         Paragraph("A* Expansions", table_hdr_style),
         Paragraph("Expansion Reduction", table_hdr_style)],
        
        [Paragraph("Baseline (<code>emu_campus.txt</code>)", table_cell_left),
         Paragraph("S &rarr; W (Student &rarr; Walton)", table_cell_left),
         Paragraph("18", table_cell_style), Paragraph("18", table_cell_style),
         Paragraph("67", table_cell_style), Paragraph("22", table_cell_bold),
         Paragraph("<b>-67.2%</b>", table_cell_bold)],

        [Paragraph("Baseline (<code>emu_campus.txt</code>)", table_cell_left),
         Paragraph("L &rarr; D (Library &rarr; Downing)", table_cell_left),
         Paragraph("22", table_cell_style), Paragraph("22", table_cell_style),
         Paragraph("79", table_cell_style), Paragraph("62", table_cell_bold),
         Paragraph("<b>-21.5%</b>", table_cell_bold)],

        [Paragraph("Baseline (<code>emu_campus.txt</code>)", table_cell_left),
         Paragraph("H &rarr; P (Harrold &rarr; Putnam)", table_cell_left),
         Paragraph("16", table_cell_style), Paragraph("16", table_cell_style),
         Paragraph("41", table_cell_style), Paragraph("16", table_cell_bold),
         Paragraph("<b>-61.0%</b>", table_cell_bold)],

        [Paragraph("Detour (<code>emu_detour.txt</code>)", table_cell_left),
         Paragraph("S &rarr; W (Student &rarr; Walton)", table_cell_left),
         Paragraph("26", table_cell_style), Paragraph("26", table_cell_style),
         Paragraph("70", table_cell_style), Paragraph("51", table_cell_bold),
         Paragraph("<b>-27.1%</b>", table_cell_bold)],

        [Paragraph("Detour (<code>emu_detour.txt</code>)", table_cell_left),
         Paragraph("L &rarr; D (Library &rarr; Downing)", table_cell_left),
         Paragraph("22", table_cell_style), Paragraph("22", table_cell_style),
         Paragraph("65", table_cell_style), Paragraph("60", table_cell_bold),
         Paragraph("<b>-7.7%</b>", table_cell_bold)],

        [Paragraph("Detour (<code>emu_detour.txt</code>)", table_cell_left),
         Paragraph("H &rarr; P (Harrold &rarr; Putnam)", table_cell_left),
         Paragraph("16", table_cell_style), Paragraph("16", table_cell_style),
         Paragraph("41", table_cell_style), Paragraph("16", table_cell_bold),
         Paragraph("<b>-61.0%</b>", table_cell_bold)]
    ]

    t1 = Table(t1_data, colWidths=[108, 126, 62, 60, 62, 60, 62])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002b49')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f8fa')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 4))

    # Figure 1: Search Node Expansions
    fig1_path = os.path.join("figures", "search_expansion_comparison.png")
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=6.8*inch, height=2.4*inch))
        story.append(Paragraph("<b>Figure 1:</b> Node expansions of BFS (uninformed) vs. A* (Manhattan heuristic) across all campus delivery benchmarks.", caption_style))

    story.append(Paragraph("Detailed Analysis & Algorithmic Comparison", h2_style))
    story.append(Paragraph(
        "<b>1. Route Length Equivalence:</b> In all six benchmark tasks, BFS and A* discover routes of identical lengths (18, 22, 16, 26, 22, 16). "
        "This empirical consistency confirms the theoretical proof: both algorithms guarantee cost-optimality on positive unit-cost grids with an admissible heuristic.<br/>"
        "<b>2. Impact of Walkway Detour:</b> In <code>emu_detour.txt</code>, walkway coordinate <i>(3, 6)</i> is obstructed. "
        "For task S &rarr; W, cell <i>(3, 6)</i> lies directly on the primary baseline corridor; its closure forces the robot along an 8-step detour around the central "
        "academic building complex (route length increases from 18 to 26). In contrast, tasks L &rarr; D (22 steps) and H &rarr; P (16 steps) remain unchanged "
        "in route length because their optimal paths do not traverse cell <i>(3, 6)</i>.<br/>"
        "<b>3. Node Expansion Reduction:</b> A* expanded substantially fewer nodes than BFS across all six scenarios. The efficiency gain is most striking "
        "for H &rarr; P on both maps, where A* expanded exactly 16 nodes—matching the path length. Because the corridor between H and P is relatively direct, "
        "the heuristic error is zero along the path (<i>h(s) = h<sup>*</sup>(s)</i>), guiding A* directly to Putnam Hall with zero wasted exploration. "
        "For Baseline S &rarr; W, A* achieved a <b>67.2% reduction</b> in expansions (22 vs. 67).<br/>"
        "<b>4. Theoretical Nuance: Does A* Always Expand Fewer Nodes Than BFS?</b> "
        "While A* dominates on these maps, <i>A* does not expand fewer nodes than BFS in every arbitrary problem</i>. "
        "When an environment features deep concave obstacles (e.g., U-shaped walls whose opening faces away from the goal), an admissible heuristic "
        "draws A* deep into the dead-end because geometric distance to the goal decreases. A* must exhaustively expand all interior nodes until "
        "<i>f = g + h</i> exceeds the cost of backing out. In contrast, BFS radiates outward in concentric shells and may locate the bypass route "
        "with fewer total node expansions than a heuristic trapped in a deep local minimum. On open or corridor-based maps, however, A* provides massive computational savings.",
        body_style
    ))

    # Page break to Page 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Part B Q-Learning, Part C Custom Map & Epsilon Study, Figure 2, Conclusion
    # =========================================================================
    story.append(Paragraph("4. Part B: Model-Free Q-Learning Formulation & Baseline Evaluation", h1_style))
    story.append(Paragraph(
        "When the robot operates without prior map access, it must learn an optimal policy through interaction. We implement tabular Q-learning with "
        "&epsilon;-greedy action selection. The environment charges a step penalty of <i>r = -1</i> for each action and grants a <i>+40</i> delivery bonus "
        "upon first arrival at the goal (terminal step <i>r = +39</i>). The episode truncates after 200 actions, yielding an undiscounted return "
        "<i>R = 40 - L</i> for an optimal <i>L</i>-step path. State-action pairs are stored in a table initialized to 0.0. The off-policy Bellman update is:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>y = r</i> &nbsp;(if terminal), &nbsp;&nbsp;&nbsp;&nbsp;<i>y = r + &gamma; max<sub>a' &in; A</sub> Q(s', a')</i> &nbsp;(otherwise)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>Q(s, a) &larr; Q(s, a) + &alpha; [ y - Q(s, a) ]</i><br/>"
        "<b>Hyperparameters:</b> Learning rate <i>&alpha; = 0.3</i>, discount <i>&gamma; = 0.95</i>, exploration <i>&epsilon; = 0.20</i>. "
        "Each task is trained across 3 independent seeds (0, 1, 2) for 2,000 episodes and evaluated over 100 greedy episodes (<i>&epsilon; = 0</i>) with learning frozen.",
        body_style
    ))

    # Table 2: Part B Baseline Q-Learning Evaluation
    story.append(Paragraph("<b>Table 2: Part B Baseline Q-Learning Evaluation Across 3 Independent Training Seeds</b>", h2_style))
    t2_data = [
        [Paragraph("Baseline Delivery Task", table_hdr_style),
         Paragraph("Target Path (<i>L</i>)", table_hdr_style),
         Paragraph("Target Return (40 - <i>L</i>)", table_hdr_style),
         Paragraph("Eval Success Rate", table_hdr_style),
         Paragraph("Eval Mean Return", table_hdr_style),
         Paragraph("Eval Mean Steps", table_hdr_style)],
        
        [Paragraph("S &rarr; W (Student &rarr; Walton)", table_cell_left),
         Paragraph("18", table_cell_style), Paragraph("22.0", table_cell_style),
         Paragraph("<b>100%</b> (1.0 &plusmn; 0.0)", table_cell_bold),
         Paragraph("<b>22.0</b> &plusmn; 0.0", table_cell_bold),
         Paragraph("<b>18.0</b> &plusmn; 0.0", table_cell_bold)],

        [Paragraph("L &rarr; D (Library &rarr; Downing)", table_cell_left),
         Paragraph("22", table_cell_style), Paragraph("18.0", table_cell_style),
         Paragraph("<b>100%</b> (1.0 &plusmn; 0.0)", table_cell_bold),
         Paragraph("<b>18.0</b> &plusmn; 0.0", table_cell_bold),
         Paragraph("<b>22.0</b> &plusmn; 0.0", table_cell_bold)],

        [Paragraph("H &rarr; P (Harrold &rarr; Putnam)", table_cell_left),
         Paragraph("16", table_cell_style), Paragraph("24.0", table_cell_style),
         Paragraph("<b>100%</b> (1.0 &plusmn; 0.0)", table_cell_bold),
         Paragraph("<b>24.0</b> &plusmn; 0.0", table_cell_bold),
         Paragraph("<b>16.0</b> &plusmn; 0.0", table_cell_bold)]
    ]
    t2 = Table(t2_data, colWidths=[150, 78, 88, 76, 76, 72])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002b49')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f8fa')]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t2)
    story.append(Paragraph(
        "<b>Baseline Discussion:</b> Across all nine independent training runs, the evaluated policy achieved a 100% success rate with zero variance. "
        "The evaluation path lengths (18, 22, 16) and observed returns (22.0, 18.0, 24.0) precisely match the global shortest paths found by BFS and A*, "
        "demonstrating that model-free Q-learning converges reliably to the optimal policy without requiring prior transition dynamics.",
        body_style
    ))

    story.append(Paragraph("5. Part C: Custom Campus Design & Epsilon Exploration Study", h1_style))
    story.append(Paragraph(
        "<b>Custom Map Design (<code>maps/my_campus.txt</code>):</b> We designed an asymmetric <i>10 &times; 15</i> grid featuring all six campus buildings "
        "(S at (1,1), W at (1,12), L at (5,1), D at (5,13), H at (9,1), P at (9,12)). The map incorporates a direct northern walkway connecting S to W "
        "(optimal length = 11 steps), an internal cyclic loop between rows 3 and 7, and multiple dead-end branches. On task S &rarr; W, BFS took 35 expansions while A* took only 11.<br/>"
        "<b>Controlled Experiment:</b> We investigated: <i>How does varying exploration &epsilon; &in; {0.05, 0.20, 0.50} impact online training returns vs. asymptotic policy optimality?</i>",
        body_style
    ))

    # Table 3: Custom Map Epsilon Experiment
    story.append(Paragraph("<b>Table 3: Custom Map S &rarr; W Performance Under Varying Exploration Rates</b>", h2_style))
    t3_data = [
        [Paragraph("Exploration Rate (&epsilon;)", table_hdr_style),
         Paragraph("Eval Success Rate", table_hdr_style),
         Paragraph("Eval Mean Return", table_hdr_style),
         Paragraph("Eval Mean Steps", table_hdr_style),
         Paragraph("Block 1 Train Return", table_hdr_style),
         Paragraph("Block 5 Train Return", table_hdr_style),
         Paragraph("Block 20 Train Return", table_hdr_style)],
        
        [Paragraph("&epsilon; = 0.05 (Low Exploration)", table_cell_left),
         Paragraph("100% (1.0 &plusmn; 0.0)", table_cell_bold),
         Paragraph("29.0 &plusmn; 0.0", table_cell_bold),
         Paragraph("11.0 &plusmn; 0.0", table_cell_bold),
         Paragraph("-3.1", table_cell_style),
         Paragraph("+28.5", table_cell_bold),
         Paragraph("+28.3", table_cell_bold)],

        [Paragraph("&epsilon; = 0.20 (Baseline)", table_cell_left),
         Paragraph("100% (1.0 &plusmn; 0.0)", table_cell_bold),
         Paragraph("29.0 &plusmn; 0.0", table_cell_bold),
         Paragraph("11.0 &plusmn; 0.0", table_cell_bold),
         Paragraph("-5.1", table_cell_style),
         Paragraph("+26.0", table_cell_style),
         Paragraph("+26.3", table_cell_style)],

        [Paragraph("&epsilon; = 0.50 (High Exploration)", table_cell_left),
         Paragraph("100% (1.0 &plusmn; 0.0)", table_cell_bold),
         Paragraph("29.0 &plusmn; 0.0", table_cell_bold),
         Paragraph("11.0 &plusmn; 0.0", table_cell_bold),
         Paragraph("-18.2", table_cell_style),
         Paragraph("+16.5", table_cell_style),
         Paragraph("+16.0", table_cell_style)]
    ]
    t3 = Table(t3_data, colWidths=[120, 70, 70, 64, 72, 72, 72])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002b49')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f8fa')]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t3)
    story.append(Spacer(1, 3))

    # Figure 2: Q-learning Curves
    fig2_path = os.path.join("figures", "q_learning_curves.png")
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=6.8*inch, height=2.1*inch))
        story.append(Paragraph("<b>Figure 2:</b> Q-learning training curves: (a) Baseline campus tasks; (b) Custom map S&rarr;W across exploration rates &epsilon; = 0.05, 0.20, 0.50.", caption_style))

    story.append(Paragraph(
        "<b>Synthesis & Key Insights:</b> (1) <i>Off-Policy Decoupling:</i> Crucially, all three exploration settings learned the exact same optimal greedy route "
        "(11 steps, return 29.0). Because Q-learning updates target the greedy choice <i>max<sub>a'</sub> Q(s', a')</i> rather than the behavior policy's selected action, "
        "asymptotic policy optimality remains immune to behavioral randomness, provided all states are adequately explored. "
        "(2) <i>Online Dithering Penalty:</i> However, online training returns vary dramatically. Under <i>&epsilon; = 0.50</i>, taking random actions 50% of the time "
        "causes severe wandering during training, depressing asymptotic training returns to ~16.0 (taking ~24 steps/episode). In contrast, <i>&epsilon; = 0.05</i> "
        "achieves near-optimal training returns (~28.4) while maintaining sufficient exploration to discover the northern corridor.",
        body_style
    ))

    story.append(Paragraph("6. Conclusion", h1_style))
    story.append(Paragraph(
        "This project successfully analyzed autonomous navigation using classical planning and reinforcement learning. In Part A, A* with the admissible "
        "Manhattan heuristic reduced node expansions by up to 67.2% relative to BFS while guaranteeing route optimality. In Part B, tabular Q-learning "
        "converged across all seeds to the identical shortest routes found by A*. In Part C, custom map experiments illustrated the fundamental trade-off "
        "between online exploration cost and off-policy asymptotic convergence.",
        body_style
    ))

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Successfully built Eagle_Delivery_Report.pdf")

if __name__ == "__main__":
    build_pdf()
