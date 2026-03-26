export type MaskingMode = 'full' | 'partial';

export interface MaskingOptions {
  mode?: MaskingMode;
  customRules?: string[];
  maskCharacter?: string;
}

export interface MaskResult {
  maskedCode: string;
  detectedSecrets: string[];
}

export function maskCode(code: string, options?: MaskingOptions): MaskResult {
  const mode = options?.mode || 'full';
  const maskChar = options?.maskCharacter || '*';
  const customRules = options?.customRules || [];
  
  const detectedSecrets = new Set<string>();

  // Helper to generate the mask string
  const createMask = (match: string) => {
    if (mode === 'full') {
      return maskChar.repeat(match.length);
    } else {
      // Partial masking: show first 3 and last 3 chars if long enough, else just mask all
      if (match.length <= 6) return maskChar.repeat(match.length);
      const start = match.slice(0, 3);
      const end = match.slice(-3);
      const middle = maskChar.repeat(match.length - 6);
      return `${start}${middle}${end}`;
    }
  };

  let maskedCode = code;

  // 1. JWT Tokens
  const jwtRegex = /ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*/g;
  maskedCode = maskedCode.replace(jwtRegex, (match) => {
    detectedSecrets.add('JWT Token');
    return createMask(match);
  });

  // 2. Exact Emails
  const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
  maskedCode = maskedCode.replace(emailRegex, (match) => {
    detectedSecrets.add('Email Address');
    return createMask(match);
  });

  // 3. Phone Numbers (Basic US/Intl format)
  const phoneRegex = /\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g;
  maskedCode = maskedCode.replace(phoneRegex, (match) => {
    // Basic filter to avoid masking IP addresses heavily or generic math
    if (match.length >= 10 && /\d{3}/.test(match)) {
      detectedSecrets.add('Phone Number');
      return createMask(match);
    }
    return match;
  });

  // 4. Common API Keys (OpenAI, AWS, Stripe)
  const apiKeyRegex = /\b(sk-[a-zA-Z0-9]{32,}|AKIA[0-9A-Z]{16}|rk_[live|test]_[a-zA-Z0-9]{24,})\b/g;
  maskedCode = maskedCode.replace(apiKeyRegex, (match) => {
    detectedSecrets.add('API Key');
    return createMask(match);
  });

  // 5. Generic Secrets (passwords, tokens, keys) using heuristics (variables with secret/key/password)
  const secretAssignRegex = /(token|password|secret|key|auth|api_key)["'\s]*[:=]\s*["']([^"'\n]+)["']/gi;
  maskedCode = maskedCode.replace(secretAssignRegex, (match, prefix, secretValue) => {
    // Only mask if the secret value looks somewhat significant (> 5 chars)
    if (secretValue.length > 5) {
      detectedSecrets.add(`Credential (${prefix.toLowerCase()})`);
      const maskedValue = createMask(secretValue);
      return match.replace(secretValue, maskedValue);
    }
    return match;
  });

  // 6. Custom Rules
  if (customRules.length > 0) {
    customRules.forEach(rule => {
      try {
        const customRegex = new RegExp(`\\b${rule}\\b`, 'gi');
        maskedCode = maskedCode.replace(customRegex, (match) => {
          detectedSecrets.add(`Custom Rule: ${rule}`);
          return createMask(match);
        });
      } catch (e) {
        // Ignore invalid custom regex
      }
    });
  }

  return {
    maskedCode,
    detectedSecrets: Array.from(detectedSecrets)
  };
}
