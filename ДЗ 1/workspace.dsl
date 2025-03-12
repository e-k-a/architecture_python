workspace {
    name "VK"
    !identifiers hierarchical

    model {

        registred_user = Person "Зарегистрированный пользователь" {
            tags "main"
        }

        unregistred_user = Person "Незарегистрированный пользователь" {
            tags "unregistred" "main"
        }

        social_network = softwareSystem "Социальная сеть" {
            tags "softwareSystem"
        }

        vk = softwareSystem "VK" {
            -> social_network "Соцсеть для общения людей"
            tags "softwareSystem"

            
            feeds = container "Система Стена"{
                technology "golang"
                tags "unregistred" "main"
            }

            messages = container "Система сообщений" {
                technology "Kotlin"
                tags "main"
            }

            monitoring = container "Система трекинга"{
                technology "Python plotly"       
            }

            search = container "Система поиска"{
                technology "python fastapi"
            }

            registry = container "Система управления доступами"{
                technology "golang"
                tags "unregistred" "main"
            }
            messages -> registry "Проверяет доступ к сообщениям" 
            registry -> feeds "Создает Стену для нового пользователя " "REST"
            registry -> monitoring "Отправляет отчет о действиях пользователя" "Queue"
            search -> registry "Выполненяется поиск по id" "REST"
            search -> registry "Выполненяется поиск по имени и фамилии" "REST"
            feeds -> registry "Проверяет доступ к Стене при загрузке" "REST"
            feeds -> monitoring "Отправляет отчет о новой записи" "Queue"



            registred_user -> vk "Тратит время"
            unregistred_user -> vk "Приходит"
            registred_user -> messages "Отправляет сообщение"
            registred_user -> search "Производит поиск по параметрам"
            registred_user -> feeds "Пишет новости"
            registred_user -> monitoring "Мониторит"
            unregistred_user -> registry "Создает аккаунт"
            unregistred_user -> feeds "Наблюдает"
      
        }

    }

    views {

        themes default

        systemContext vk "SystemContext" {
            include *
            autoLayout
        }

        container vk "Containers" {
            include *
            autoLayout
        }

        container vk "c2unreliazed" {
            include "element.tag==unregistred"
            autoLayout
        }

        dynamic vk "Registrate" "Регистрация" {
            unregistred_user -> vk.registry "Регистрируется"
            vk.registry -> vk.monitoring "Передает отчет о пользователей"
            autoLayout
        }

        styles {
            element "Person" {
                shape Person
                background #FF00BF
            }

            element "Container" {
                background #F8337E
            }

            element "softwareSystem" {
                background #BD1189
            }


        }

    }

}