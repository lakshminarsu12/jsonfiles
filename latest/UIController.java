@Controller
@RequestMapping("/ui/prompts")
public class UIController {

    @Autowired
    private AskAttPromptRepository repository;

    @GetMapping
    public String showPrompts(Model model) {
        List<AskAttPrompt> prompts = repository.findAll();
        model.addAttribute("prompts", prompts);
        model.addAttribute("prompt", new AskAttPrompt());
        return "prompts";
    }

    @PostMapping("/add")
    public String addPrompt(@ModelAttribute AskAttPrompt prompt) {
        repository.save(prompt);
        return "redirect:/ui/prompts";
    }

    @PostMapping("/update")
    public String updatePrompt(@ModelAttribute AskAttPrompt updatedPrompt) {
        repository.findByMeaningfulName(updatedPrompt.getMeaningfulName())
                .ifPresent(existing -> {
                    existing.setUserPrompt(updatedPrompt.getUserPrompt());
                    existing.setSystemPrompt(updatedPrompt.getSystemPrompt());
                    existing.setPromptType(updatedPrompt.getPromptType());
                    repository.save(existing);
                });
        return "redirect:/ui/prompts";
    }

    @GetMapping("/delete/{meaningfulName}")
    public String deletePrompt(@PathVariable String meaningfulName) {
        repository.findByMeaningfulName(meaningfulName)
                .ifPresent(repository::delete);
        return "redirect:/ui/prompts";
    }
}
