const EMOJI_RE = /\p{Extended_Pictographic}/u;

export default {
  meta: { type: "suggestion", docs: { description: "Reject emoji in code, comments and UI copy (SR-006)." } },
  create(context: any) {
    const report = (node: any, where: string) => {
      context.report({ node, message: `slop-local/no-emoji: emoji in ${where} is not allowed — use plain text` });
    };
    return {
      Literal(node: any) {
        if (typeof node.value === "string" && EMOJI_RE.test(node.raw ?? "")) report(node, "string literal");
      },
      "Program:exit"(node: any) {
        for (const c of context.sourceCode.getAllComments()) {
          if (EMOJI_RE.test(c.value)) report(node, "comment");
        }
      },
    };
  },
};
