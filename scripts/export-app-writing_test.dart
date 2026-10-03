import 'dart:convert';
import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:hanja_app/hanzi_painter.dart';
import 'package:hanja_app/handwriting/stroke_scorer.dart';
void main() {
 test('export actual app glyph transforms and scoring evidence', () {
  final output = Platform.environment['HANJA_SITE_EXPORT_DIR']!;
  final glyphs=<String,dynamic>{};
  final cases=<Map<String,dynamic>>[];
  const scorer=StrokeScorer();
  for(final char in ['明','木']) {
   final data=jsonDecode(File('assets/hanzi/$char.json').readAsStringSync()) as Map<String,dynamic>;
   final c=HanziCharacter.fromJson(data);
   final fit=GlyphFit.of(c);
   glyphs[char]={'scale':fit.scale,'center':[fit.center.dx,fit.center.dy]};
   for(var i=0;i<c.medians.length;i++) {
    final expected=c.medians[i].map((p)=>fit.toCanvas(p,600)).toList();
    final inputs=[expected,expected.reversed.toList(),expected.map((p)=>p+const Offset(25,-20)).toList(),expected.map((p)=>p+const Offset(180,180)).toList(),expected.take(2).toList()];
    for(var j=0;j<inputs.length;j++) {
     final score=scorer.score(user:inputs[j],expected:expected,canvasSize:600);
     cases.add({'id':'$char-$i-$j','user':inputs[j].map((p)=>[p.dx,p.dy]).toList(),'expected':expected.map((p)=>[p.dx,p.dy]).toList(),'canvasSize':600,'score':{'frechet':score.frechet,'directionOk':score.directionOk,'startPointOk':score.startPointOk,'passed':score.passed,'accuracy':score.accuracy}});
    }
   }
  }
  File('$output/glyph-fits.json').writeAsStringSync(jsonEncode(glyphs));
  Directory('$output/tests').createSync();
  File('$output/tests/app-scorer-fixtures.json').writeAsStringSync(jsonEncode(cases));
 });
}
