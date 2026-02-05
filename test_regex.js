
const testCases = [
    "📚 总体架构 (The Grand Architecture)",
    "Volume I: 算法思维与决策 (Algorithmic Thinking for Decision Makers)",
    "单纯的中文标题",
    "Pure English Title",
    "Mixed Content: 这是一个混合 (This is mixed)"
];

function simulateProcessing(text) {
    console.log(`\nOriginal: "${text}"`);
    
    // Pattern 1: Parentheses separation "Chinese (English)"
    // Looking for: Chinese char followed by english in parens OR English followed by Chinese in parens?
    // User format seems to be: ZH (EN)
    const mixedMatch = text.match(/([\s\S]*?)(\s*\(([\x00-\x7F]+)\))/); 
    // [\x00-\x7F] approximates ASCII/English. 
    
    if (mixedMatch) {
        const part1 = mixedMatch[1];
        const part2 = mixedMatch[2]; // Includes parens
        
        const isPart1Zh = /[\u4e00-\u9fa5]/.test(part1);
        const isPart2Zh = /[\u4e00-\u9fa5]/.test(part2);
        
        // Only split if they look like different languages
        if (isPart1Zh !== isPart2Zh) {
            console.log(`  Split result:`);
            console.log(`  Span 1 (${isPart1Zh ? 'ZH' : 'EN'}): "${part1.trim()}"`);
            console.log(`  Span 2 (${isPart2Zh ? 'ZH' : 'EN'}): "${part2.trim()}"`);
            return;
        }
    }
    
    // Fallback: Whole classification
    const isZh = /[\u4e00-\u9fa5]/.test(text);
    console.log(`  Whole block (${isZh ? 'ZH' : 'EN'}): "${text}"`);
}

testCases.forEach(simulateProcessing);
