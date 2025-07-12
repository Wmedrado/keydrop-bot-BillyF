import json
import time
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ActionRecorder:
    """Simple DOM action recorder for Playwright pages."""

    def __init__(self, output_file: str = None):
        self.output_file = Path(output_file or Path(__file__).parent / "last_actions.json")
        self.actions: List[Dict[str, float]] = []
        self.page = None

    async def start(self, page):
        """Start capturing click selectors from the given page."""
        self.page = page
        await page.expose_function("recordAction", self._record_action)
        await page.evaluate(
            """
            (() => {
                function getPath(el){
                    const path=[];
                    while(el){
                        let part=el.nodeName.toLowerCase();
                        if(el.id) part+='#'+el.id;
                        if(el.className) part+='.'+Array.from(el.classList).join('.');
                        path.unshift(part);
                        el=el.parentElement;
                    }
                    return path.join(' > ');
                }
                document.addEventListener('click', e => {
                    window.recordAction(getPath(e.target));
                }, {capture:true});
            })();
            """
        )

    async def _record_action(self, selector: str):
        self.actions.append({"selector": selector, "timestamp": time.time()})

    async def stop(self):
        """Stop recording and save actions."""
        if self.actions:
            try:
                with self.output_file.open("w", encoding="utf-8") as f:
                    json.dump(self.actions, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error("Erro ao salvar ações aprendidas: %s", e)
