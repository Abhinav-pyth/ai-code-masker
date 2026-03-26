import { NextRequest, NextResponse } from 'next/server';
import { maskCode, MaskingOptions } from '@/lib/masker';
import { obfuscateIdentifiers, unmaskContent } from '@/lib/obfuscator';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { code, rules, mode, obfuscate, language, action, mapping } = body;

    if (typeof code !== 'string') {
      return NextResponse.json(
        { error: 'Code must be a string' },
        { status: 400 }
      );
    }

    if (action === 'unmask') {
      if (!mapping) {
         return NextResponse.json({ error: 'Mapping required for unmasking' }, { status: 400 });
      }
      const restored = unmaskContent(code, mapping, language || 'js');
      return NextResponse.json({ unmaskedCode: restored });
    }

    const options: MaskingOptions = {
      mode: mode || 'full',
      customRules: Array.isArray(rules) ? rules : [],
    };

    // First detect and mask hardcoded secrets
    const result = maskCode(code, options);
    
    // Then optionally obfuscate all business identifiers
    let finalMapping = null;
    if (obfuscate) {
      const obfResult = obfuscateIdentifiers(result.maskedCode, language || 'js');
      result.maskedCode = obfResult.obfuscatedContent;
      finalMapping = obfResult.mapping;
    }

    return NextResponse.json({
      ...result,
      mapping: finalMapping
    });
  } catch (error) {
    console.error('API Masking Error:', error);
    return NextResponse.json(
      { error: 'Internal Server Error processing request' },
      { status: 500 }
    );
  }
}
