import { normalize, resolve } from 'node:path';

function fileName(value) {
  const path = normalize(resolve(value));
  return process.platform === 'win32' ? path.toLowerCase() : path;
}

export default async function* report(events) {
  const path = [];
  let summary;
  yield JSON.stringify({ kind: 'header', schema: 1 }) + '\n';
  for await (const { type, data } of events) {
    if (type === 'test:start') {
      if (data.nesting !== path.length) throw new Error('Unexpected Node test nesting');
      path.push(data.name);
    } else if (type === 'test:pass' || type === 'test:fail') {
      if (data.nesting !== path.length - 1 || path.at(-1) !== data.name) {
        throw new Error('Node result has no matching test start');
      }
      let kind = data.details.type;
      if (kind === 'test' && data.nesting === 0 && data.file
          && fileName(data.name) === fileName(data.file)) {
        // Node reports a file as passing when its filter selected no tests.
        kind = 'file';
      }
      const status = type === 'test:pass' && !data.skip && !data.todo ? 'passed' : 'unpassed';
      const reason = data.details.error?.stack ?? data.details.error?.message ?? data.skip ?? data.todo;
      yield JSON.stringify({ kind, path, status, file: data.file, line: data.line, reason }) + '\n';
      path.pop();
    } else if (type === 'test:stdout' || type === 'test:stderr') {
      yield JSON.stringify({ kind: 'output', stream: type, file: data.file, message: data.message }) + '\n';
    } else if (type === 'test:summary' && data.file === undefined) {
      if (summary) throw new Error('Multiple Node test run summaries');
      summary = { kind: 'summary', success: data.success, counts: data.counts };
    }
  }
  if (path.length || !summary) throw new Error('Incomplete Node test event stream');
  yield JSON.stringify(summary) + '\n';
}
